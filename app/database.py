from dataclasses import dataclass, field
from threading import Lock
from typing import NoReturn, Union


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
    username: str
    password: str
    id_counter: int = 0
    id: int = field(init=False)

    def __post_init__(self):
        self.id = User.id_counter
        User.id_counter += 1


class Database(metaclass=DatabaseMeta):
    users = {}
    _lock: Lock = Lock()

    @staticmethod
    async def add_user(username: str, hashed_password: str) -> NoReturn:
        new_user = User(
            username=username,
            password=hashed_password
        )
        with Database._lock:
            Database.users[new_user.username] = new_user.password


    @staticmethod
    async def find_user_by_username(username: str) -> Union[User, None]:
        if username in Database.users:
            password = Database.users.get(username)
            user = User(username=username, password=password)
            return user
        else:
            return None
