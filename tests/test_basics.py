from lazymappingstorage import hello2, LazyStorageObject, LazyMappingStorage
import pytest
from dataclasses import dataclass


@pytest.fixture
def obj():
    obj = LazyStorageObject()
    return obj


@pytest.fixture
def objdata():
    obj = LazyStorageObject({"id": 23})
    return obj

@pytest.fixture
def MyObjClass():
    class MyObj(LazyStorageObject):
        id: str = 4
    return MyObj

@pytest.fixture
def UserClass():
    class UserClass(LazyStorageObject):
        pass
    return UserClass




def test_create_new_class():
    #    @dataclass
    class MyObj(LazyStorageObject):
        id: str = 4

    o = MyObj()
    assert o.id == 4


def test_first():
    assert True

def test_lazy_init():
    o=LazyStorageObject(desc="description")
    assert o.desc=="description"


def test_init_object(MyObjClass):
    o = MyObjClass(id=2)
    assert o.id == 2


def test_update(objdata):
    objdata.update({"id": 2})
    assert objdata.id == 2


def test_from_dict():
    map=LazyMappingStorage(file="users.yaml")
    map.from_dict({"1": {"name": "Andi"}, "2": {"name": "Peter"}})
    assert map["1"].name=="Andi"

def test_from_dict2():
    map=LazyMappingStorage(file="users.yaml")
    map.from_dict({"1": {"name": "Andi"}, "2": {"name": "Peter"}})
    assert type(map["1"]) is LazyStorageObject


def test_filename_class():
    class Map1(LazyMappingStorage):
        filename="users.yaml"
    m=Map1()
    assert m.filename == "users.yaml"

    
def test_usermanager():
   class User(LazyStorageObject):
       pass
   class Update:
       pass
   class UserManager(LazyMappingStorage):
    filename = "users.yaml"
    object_class=User
    def __init__(self):
        super().__init__()#file="users.yaml")
        self.from_file()

    def from_dict(self,d):
        for k in d:
            self[k]=User(**d[k])
    def __getitem__(self, key):
        if isinstance(key, Update):
            u=self.__getitem__(get_from_id(key))
            u.load_from(key)
            return u
        u=super().__getitem__(key)
        if u is None:
            u=User(id=key)
            self[key]=u
        return u
   um=UserManager()
   assert isinstance(um,UserManager)
#   assert um.__file == "users.yaml"
   assert um.filename=="users.yaml"
   um.to_file()
