from abc import ABC, abstractmethod
import pickle
import json


class Packager(ABC):
    def __init__(self, terminator="\n"):
        self.terminator = terminator

    @abstractmethod
    def pack(self, data, terminate=True): ...

    @abstractmethod
    def unpack(self, data): ...


class SeparatorPackager(Packager):
    def __init__(self, sep_major="|", sep_minor=";", terminator="\n"):
        """ """
        super().__init__(terminator)
        # Set the major and minor separators
        self.sep_major = sep_major
        self.sep_minor = sep_minor

    def pack(self, data, terminate=True):
        # Pack some data into a separated string
        packed_data = ""
        if not isinstance(data[0], (list, tuple)):
            data = [data]
        for item in data:
            packed_data += self.sep_minor.join(map(str, item))
            packed_data += self.sep_major
        if terminate:
            packed_data += self.terminator
        return packed_data

    def unpack(self, data):
        # Unpack some separated data into a list of lists
        # Remove the terminator from the end of the data if present
        data = data.removesuffix(self.terminator).removesuffix(self.sep_major)
        items = data.split(self.sep_major)
        unpacked = []
        for item in items:  # Exclude the last empty item after the last separator
            values = item.split(self.sep_minor)
            unpacked.append(values)
        if len(unpacked) == 1:
            unpacked = unpacked[0]
        return unpacked


class PicklerPackager(Packager):
    def pack(self, data, terminate=True):
        return pickle.dumps(data, protocol=pickle.HIGHEST_PROTOCOL) + (
            self.terminator if terminate else b""
        )

    def unpack(self, data):
        return pickle.loads(data)


class JSONPackager(Packager):
    def pack(self, data, terminate=True):
        return json.dumps(data) + (self.terminator if terminate else "")

    def unpack(self, data):
        if data := data.removesuffix(self.terminator):
            return json.loads(data)
