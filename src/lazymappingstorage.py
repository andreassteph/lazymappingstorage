import yaml
from collections.abc import Mapping
from dataclasses import asdict, dataclass


def hello2():
    print("hello2")


@dataclass
class LazyStorageObject:
    def __init__(self, data={},**kwargs):
        for key, value in data.items():
            setattr(self, key, value)
        for key, value in kwargs.items():
            setattr(self, key, value)
        
    def asdict(self):
        return asdict(self)

    def update(self, new):
        if not new: return
        for key, value in new.items():
            if hasattr(self, key):
                setattr(self, key, value)


class LazyMappingStorage(Mapping):
    object_class = LazyStorageObject
    
    def __init__(self, file=None):
        self.data = dict()
        if file:
            self.filename=file
        elif not hasattr(self, "filename")  and not hasattr(self.__class__,"filename"):
            self.filename=None
        self.from_file()  # load data from a file

    
    def asdict(self):
        return {k: self[k].asdict() for k in self}

    def from_dict(self, d):
        for key, value in d.items():
            self.data[key]=self.__class__.object_class(**value)

    def to_file(self):
        if self.filename is None: return
        with open(self.filename, "w") as f:
            f.write(yaml.dump(self.asdict()))

    def from_file(self, filename=None):
        if filename: self.filename=filename
        if not self.filename: raise Exception()
        try:
            with open(self.filename, "r") as f:
                d = yaml.safe_load(f) or {}
        except FileNotFoundError:
            with open(self.filename, "w") as f:
                f.write("")
                d={}
        self.from_dict(d)

    def __getitem__(self, key):
        if not key in self.data:
            self[key]=self.__class__.object_class()
        return self.data.get(key)
    
    def __setitem__(self, key, data):
        if not isinstance(data, LazyStorageObject) and isinstance(data,dict):
            data=self.object_class(**data)
        if not isinstance(data, LazyStorageObject):
            raise TypeError("""data elements should
             be derived from LazyStorageObject""")
        self.data[key] = data
        return self.data[key]

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)
