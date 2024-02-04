from collections import deque
import logging
from copy import deepcopy

from buffered.packager import Packager, SeparatorPackager, JSONPackager

logger = logging.getLogger(__name__)


class Buffer:
    """
    A buffer class that stores data in a deque

    Example:
    >>> buffer = Buffer()
    >>> buffer.add(1)
    >>> buffer.add(2)
    >>> buffer.add(3)
    >>> buffer.add(4)
    >>> buffer.add(5)
    >>> buffer
    Buffer(deque([1, 2, 3, 4, 5], maxlen=4096))
    >>> buffer.get_copy()
    Buffer(deque([1, 2, 3, 4, 5], maxlen=4096))
    >>> buffer.get_size()
    5
    >>> buffer.not_empty()
    True
    >>> buffer.dump()
    [1, 2, 3, 4, 5]
    >>> buffer.peek()
    [1, 2, 3, 4, 5]
    >>> buffer.peek(2)
    3

    """

    def __init__(self, data=None, maxlen=4096):
        data = data or []
        self.buffer = deque(data, maxlen=maxlen)

    def add(self, data):
        try:
            if isinstance(data[0], list):
                self.buffer.extend(data)
        except TypeError:
            pass
        self.buffer.append(data)

    def append(self, data):
        self.add(data)

    def reinsert(self, data):
        try:
            if isinstance(data[0], list):
                self.buffer.extendleft(data)
        except TypeError:
            pass
            self.buffer.appendleft(data)

    def clear(self):
        self.buffer.clear()

    def get_copy(self):
        return deepcopy(self)

    def get_size(self):
        return len(self.buffer)

    def not_empty(self):
        return len(self.buffer) > 0

    def dump(self, maximum=None):
        maximum = maximum or len(self.buffer)
        return [self.buffer.popleft() for _ in range(min(maximum, len(self.buffer)))]

    def peek(self, idx=None):
        if idx is not None:
            return self.buffer[idx]
        return list(self.buffer)

    def __next__(self):
        return self.buffer.popleft()

    def __iter__(self):
        return self

    def __len__(self):
        return len(self.buffer)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.buffer})"

    def __str__(self):
        return f"{self.__class__.__name__}({self.buffer})"

    def __getitem__(self, index):
        return self.buffer[index]

    def __setitem__(self, index, value):
        self.buffer[index] = value


class PackagedBuffer(Buffer):
    def __init__(
        self,
        data=None,
        packager: Packager = None,
        maxlen=4096,
        terminator="\0",
    ):
        data = data or []
        super().__init__(data, maxlen=maxlen)
        self.packager = packager or JSONPackager()
        self.terminator = terminator
        self.len_terminator = len(terminator)

    def _pack(self, data, terminate=True):
        if self.packager:
            return self.packager.pack(data, terminate)
        return data

    def _unpack(self, data):
        if self.packager:
            return self.packager.unpack(data)
        return data

    def next_packed(self, terminate=True):
        next_data = next(self)
        # pack the next data before returning it
        return self.packager.pack(next_data, terminate)

    def next_unpacked(self):
        next_data = next(self)
        return self.packager.unpack(next_data)

    def _dump_with_func(self, next_func, maximum=None):
        maximum = maximum or len(self.buffer)
        dump_length = min(maximum, len(self.buffer))
        return [next_func() for _ in range(dump_length)]

    def dump_packed(self, maximum=None):
        return self._dump_with_func(self.next_packed, maximum)

    def dump_unpacked(self, maximum=None):
        if isinstance(self.peek(idx=0), list):
            return self.dump(maximum)
        return self._dump_with_func(self.next_unpacked, maximum)


# TODO Implement this
# class PacketOptimizedBuffer(PackagedBuffer):
#     def __init__(
#         self,
#         data=None,
#         packager: Packager = None,
#         maxlen=4096,
#         max_packet_size=4096,
#         terminator="\0",
#     ):
#         """ """

#         data = data or []
#         super().__init__(data, maxlen=maxlen)
#         self.packager = packager
#         self.max_packet_size = max_packet_size
#         self.terminator = terminator
#         self.len_terminator = len(terminator)

#     def next_packed(self, max_packet_size=None):
#         # If max_packet_size is not specified, use the default value
#         max_packet_size = max_packet_size or self.max_packet_size
#         packet = ""
#         # Get the next package using the PackagedBuffer method
#         data = super().next_packed(terminate=False)
#         # Check if the next package is too large to fit in the specified packet size
#         if len(data) > max_packet_size:
#             raise ValueError(
#                 f"Maximum packet size of {max_packet_size} too small. Data is {len(data)} bytes long."
#             )
#         # Check if adding the next package to the packet will exceed the maximum packet size
#         while len(packet) + len(data) + self.len_terminator <= max_packet_size:
#             # Add the next package to the packet
#             packet += data
#             try:
#                 # Try get the next package. If there are no more packages, break the loop
#                 data = super().next_packed(terminate=False)
#             except IndexError:
#                 break
#         else:
#             data = self._unpack(data)
#             self.reinsert(data)
#         # Add the terminator to the packet before returning it
#         return packet + self.terminator

#     def dump_packed(self, max_packet_size=None):
#         max_packet_size = max_packet_size or self.max_packet_size
#         packets = []
#         packet = self.next_packed(max_packet_size)
#         while packet:
#             packets.append(packet)
#             packet = self.next_packed(max_packet_size)
#         return packets


# def test1():
#     data = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]
#     packager = SeparatorPackager(sep_major="|", sep_minor=";")
#     datastream = PacketOptimizedBuffer(data, packager=packager)
#     print(datastream)
#     packet = datastream.next_packet(1024)
#     print()
#     print(f"{packet} of length{len(packet)}")
#     print(f"unpacked data: {packager.unpack(packet)}")

#     datastream = PacketOptimizedBuffer(data, packager=packager)
#     packet = datastream.next_packet(10)
#     print(f"{packet} of length{len(packet)}")


def main():
    def modify_buffer(buffer: Buffer) -> None:
        buffer.add(1)
        buffer.add(2)
        buffer.add(3)
        buffer.add(4)
        buffer.add(5)

    buffer = Buffer()
    print(buffer)
    modify_buffer(buffer)
    print(buffer)


if __name__ == "__main__":
    main()
