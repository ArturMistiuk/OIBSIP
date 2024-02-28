from dataclasses import dataclass
from threading import Lock
from typing import NoReturn, Union
from app.exceptions import UserIsNotPresentError

class DatabaseMeta(type):
    _instances = {}

    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


@dataclass
class User:
    id: int
    username: str
    password: str


class Database(metaclass=DatabaseMeta):
    users = {}
    _lock: Lock = Lock()
    id_counter: int = 0

    @staticmethod
    async def add_user(username: str, hashed_password: str) -> NoReturn:
        new_user = User(
            id=Database.id_counter,
            username=username,
            password=hashed_password
        )
        with Database._lock:
            Database.id_counter += 1
            Database.users[new_user.id] = (new_user.username, new_user.password)


    @staticmethod
    async def find_user_by_username(username: str) -> Union[User, None]:
        for user_id, (user_username, user_password) in Database.users.items():
            if username == user_username:
                return User(id=user_id, username=user_username, password=user_password)
        return None

    @staticmethod
    async def find_user_by_id(user_id: int) -> Union[User, None]:
        user_data: tuple = Database.users.get(user_id)
        if user_data:
            return User(id=user_id, username=user_data[0], password=user_data[1])
