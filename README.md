asdf

This is intended to provide a very simple way to manage data and store them to file.
The main design principle is to provide as many sensible defaults as possible.

#Usage

```python

class User(LazyStorageObject):
      id: int
      name: str
      authorized: bool = False
class UserMapping(LazyMappingStorage):
      object_class=User
      filename="users.yaml"

users=UserMapping()

u=users[1]
u.name="andi"
users.to_file()
	
```
#Install


#Development
git clone
pip install -e

pip install -e .[dev]
