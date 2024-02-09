#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Matthew Davidson
# Created Date: 2024-02-02
# Copyright © 2024 Davidson Engineering Ltd.
# ---------------------------------------------------------------------------
"""
Buffered package.

This package provides a set of classes for buffering data.

The Buffer class is a simple buffer that stores data in a deque.

"""
# ---------------------------------------------------------------------------

from collections import deque
import logging
from copy import deepcopy
from typing import Any, Callable, Optional

from buffered.packager import Packager, JSONPackager

logger = logging.getLogger(__name__)


class Buffer(deque):
    """
    A buffer class that stores data in a deque

    Args:
        data (list, tuple, set, dict, optional): Data to initialize the buffer with. Defaults to None.
        maxlen (int, optional): The maximum length of the buffer. Defaults to 4096.

    """

    def __init__(self, data: Optional[Any] = None, maxlen: int = 4096) -> None:
        data = data or []
        super().__init__(data, maxlen=maxlen)

    def _append(self, data: Any, _append_func: Callable) -> None:
        if isinstance(data, (list, tuple, set)):
            try:
                if isinstance(data[0], (list, tuple, set, dict)):
                    # If data is a list of lists, add each list to the buffer
                    for el in data:
                        _append_func(el)
                elif isinstance(data[0], (int, float, str)):
                    # If data is a list of non-lists, add the list to the buffer
                    _append_func(data)
            except (KeyError, ValueError):
                _append_func(data)
        else:
            _append_func(data)

    def put(self, data: Any) -> None:
        self._append(data, self.append)

    def putback(self, data: Any) -> None:
        self._append(data, self.appendleft)

    def get(self, index: Optional[int] = None) -> Any:
        if self.empty():
            return None
        if index is not None:
            try:
                item = self[index]
                self.remove(item)
                return item
            except IndexError as e:
                raise IndexError("Index is out of range") from e
        else:
            try:
                return self.popleft()
            except IndexError:
                return None

    def copy(self) -> "Buffer":
        return deepcopy(self)

    def size(self) -> int:
        return len(self)

    def not_empty(self) -> bool:
        return self.size() > 0

    def empty(self) -> bool:
        return self.size() == 0

    def dump(self, max: Optional[int] = None) -> list:
        max = max or self.size()
        if max == -1:
            return list(self)
        length = min(max, self.size())
        return [self.popleft() for _ in range(length)]

    def peek(self, index: int = 0) -> Any:
        if self.empty():
            return None
        try:
            return self[index]
        except IndexError as e:
            message = f"Index {index} is out of range for buffer of length {len(self)}"
            logging.error(f"{self.__class__.__name__} peek failed with {message}. {e}")
            raise IndexError(message) from e

    def __repr__(self) -> str:
        try:
            next_item = self.peek(0)
            last_item = self.peek(-1)
        except IndexError:
            next_item = None
            last_item = None
        return f"{self.__class__.__name__}({next_item} ... {last_item}, len={self.size()}/{self.maxlen})"

    def __str__(self) -> str:
        return self.__repr__()


class PackagedBuffer(Buffer):
    def __init__(
        self,
        data: Any = None,
        packager: Packager = None,
        maxlen: int = 4096,
        terminator: str = "\n",
    ) -> None:
        data = data or []
        super().__init__(data, maxlen=maxlen)
        self.packager = packager or JSONPackager()
        self.terminator = terminator

    def _pack(self, data, terminate: bool = True) -> str:
        if self.packager:
            return self.packager.pack(data, terminate)
        return data

    def _unpack(self, data: Any) -> Any:
        if self.packager:
            return self.packager.unpack(data)
        return data

    def next_packed(self, terminate: bool = True) -> str:
        next_data = self.get()
        # pack the next data before returning it
        return self.packager.pack(next_data, terminate)

    def next_unpacked(self) -> Any:
        next_data = self.get()
        return self.packager.unpack(next_data)

    def _dump_with_func(self, next_func: Callable, max: Optional[int] = None) -> list:
        max = max or len(self)
        dump_length = min(max, len(self))
        return [next_func() for _ in range(dump_length)]

    def dump_packed(self, max: Optional[int] = None):
        return self._dump_with_func(self.next_packed, max)

    def dump_unpacked(self, max: Optional[int] = None):
        if isinstance(self.peek(index=0), list):
            return self.dump(max)
        return self._dump_with_func(self.next_unpacked, max)


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
