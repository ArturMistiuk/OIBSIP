import bcrypt

from app.database import Database


def make_hash_password(password: str) -> str:
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash_password = bcrypt.hashpw(password_bytes, salt)
    return hash_password.decode('utf-8')


def verify_password(password: str, hashed_password: str) -> bool:
    password_bytes = password.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')
    check = bcrypt.checkpw(password_bytes, hashed_password_bytes)
    return check


async def authenticate_user(username: str, password: str):
    user = await Database.find_user_by_username(username)
    if user and verify_password(password, user.password):
        return user
