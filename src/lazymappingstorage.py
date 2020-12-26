import yaml
from collections.abc import Mapping
from dataclasses import asdict, dataclass


def hello2():
    print("hello2")


@dataclass
class SaveFileObject:
    def __init__(self, data={}):
        for key, value in data.items():
            setattr(self, key, value)

    def asdict(self):
        return asdict(self)

    def update(self, new):
        if new is None:
            new = {}
        for key, value in new.items():
            if hasattr(self, key):
                setattr(self, key, value)


class SaveFileMapping(Mapping):
    __file = None

    def __init__(self, file=None):
        self.data = dict()
        self.__file = file  # set file path
        self.from_file()  # load data from a file

    def asdict(self):
        return {k: self[k].asdict() for k in self}

    def from_dict(self, d):
        pass

    def to_file(self, fn=None):
        if fn is None:
            fn = self.__file
        with open(fn, "w") as f:
            f.write(yaml.dump(self.asdict()))

    def from_file(self, fn=None):
        if fn is None:
            fn = self.__file
        if fn is None: return
        try:
            with open(fn, "r") as f:
                d = yaml.load(f, Loader=yaml.Loader) or {}
        except FileNotFoundError:
            with open(fn, "w") as f:
                f.write("")
                d={}
        self.from_dict(d)

    def __getitem__(self, key):
        return self.data.get(key, None)

    def __setitem__(self, key, data):
        if not isinstance(data, SaveFileObject):
            raise TypeError("""data elements should
             be derived from SaveFileObject""")
        if not callable(getattr(data, "asdict", None)):
            raise TypeError(
                """Dataelements need a method asdict that returns
                a dict this should be out of the box if you use dataclasses"""
            )

        self.data[key] = data
        return self.data[key]

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)
