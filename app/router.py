from fastapi import APIRouter, Response, status

from app.schemas import SUserRegistration
from app.database import Database


router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)


@router.post('/register')
async def register_user(user_register_data: SUserRegistration) -> Response:
    await Database.add_user(username=user_register_data.username, password=user_register_data.password)
    return Response(status_code=status.HTTP_201_CREATED)


