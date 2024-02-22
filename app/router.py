from fastapi import APIRouter, Response, status

from app.schemas import SUserRegistration
from app.database import Database
from app.exceptions import UserAlreadyExistsError


router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)


@router.post('/register')
async def register_user(user_register_data: SUserRegistration) -> Response:
    existing_user = await Database.find_user_by_username(user_register_data.username)
    if existing_user:
        raise UserAlreadyExistsError
    await Database.add_user(username=user_register_data.username, password=user_register_data.password)
    return Response(status_code=status.HTTP_201_CREATED)


@router.post('/login')
async def login_user():
    pass
