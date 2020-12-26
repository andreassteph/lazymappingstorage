from lazymappingstorage import hello2, LazyStorageObject, LazyMappingStorage
import pytest

class UserClass(LazyStorageObject):
    a: int = 0
    name: str
    def calc(self, a):
        self.a=self.a+a

class UserManagerClass(LazyMappingStorage):
    filename="users.yaml"
    object_class = UserClass
    
@pytest.fixture
def UserManager():
    return UserManagerClass()

@pytest.fixture
def user():
    c=UserClass()
    return c()

def test_init():
    u=UserClass()
    assert isinstance(u,LazyStorageObject)

def test_filename(UserManager):
    assert UserManager.filename == "users.yaml"

def test_create_object(UserManager):
    assert isinstance(UserManager["sdf"], UserClass)


def test_file():
    users=UserManagerClass()
    u=users[1]
    u.name="Andi"
    users.to_file()
