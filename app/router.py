from fastapi import APIRouter, Response, status

from app.schemas import SUserRegistration, SUserLogin
from app.database import Database
from app.exceptions import UserAlreadyExistsError, IncorrectUsernameOrPasswordError
from app.auth import make_hash_password, authenticate_user


router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)


@router.post('/register')
async def register_user(user_data: SUserRegistration) -> Response:
    existing_user = await Database.find_user_by_username(user_data.username)
    if existing_user:
        raise UserAlreadyExistsError
    hashed_password = make_hash_password(user_data.password)
    await Database.add_user(username=user_data.username, hashed_password=hashed_password)
    return Response(status_code=status.HTTP_201_CREATED)


@router.post('/login')
async def login_user(user_data: SUserLogin):
    user = await authenticate_user(user_data.username, user_data.password)
    if not user:
        raise IncorrectUsernameOrPasswordError
    return user
