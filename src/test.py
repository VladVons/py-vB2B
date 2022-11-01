from Inc.DataClass import DataClass, _Repr


@DataClass
class TUser():
    Name: str
    Age: int

User = TUser('Vlad', 51)
print(User)
print(_Repr(User))

