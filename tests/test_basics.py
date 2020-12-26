from lazymappingstorage import hello2, SaveFileObject,SaveFileMapping
import pytest
from dataclasses import dataclass


@pytest.fixture
def obj():
    obj = SaveFileObject()
    return obj


@pytest.fixture
def objdata():
    obj = SaveFileObject({"id": 23})
    return obj


def test_create_new_class():
    #    @dataclass
    class MyObj(SaveFileObject):
        id: str = 4

    o = MyObj()
    assert o.id == 4


def test_first():
    assert True


def test_init_object():
    o = SaveFileObject({"id": 2})
    assert o.id == 2


def test_update(objdata):
    objdata.update({"id": 2})
    assert objdata.id == 2

def test_usermanager():
   class UserManager(SaveFileMapping):
    def __init__(self):
        super().__init__(file="users.yaml")
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
