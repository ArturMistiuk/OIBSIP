from dataclasses import dataclass, field
from threading import Lock

from app.services import make_hash_password

@dataclass
class User:
    username: str
    password: str
    id_counter: int = 0
    id: int = field(init=False)

    def __post_init__(self):
        self.id = User.id_counter
        User.id_counter += 1


class DatabaseMeta(type):
    _instances = {}

    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class Database(metaclass=DatabaseMeta):
    users = {}
    _lock: Lock = Lock()


    @staticmethod
    async def add_user(username: str, password: str):
        hashed_password = make_hash_password(password)
        new_user = User(
            username=username,
            password=hashed_password
        )
        print(new_user.id)
        with Database._lock:
            if new_user.username in Database.users:
                raise ValueError('User with this username already exists!')
            Database.users[new_user.username] = new_user.password
            return Database.users
