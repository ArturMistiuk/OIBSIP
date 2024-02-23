from fastapi import HTTPException, status


class MainError(HTTPException):
    status_code = 500
    detail = ''

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsError(MainError):
    status_code = status.HTTP_409_CONFLICT
    detail = 'User with this username already exists'


class IncorrectUsernameOrPasswordError(MainError):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Incorrect username or password'
