from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Union

from app.database import User


class SUserRegistration(BaseModel):
    username: str = Field(min_length=4, max_length=20)
    password: str = Field(min_length=7, max_length=25)
    confirm_password: str = Field(min_length=7, max_length=25)


    @field_validator('confirm_password', 'password', 'username')
    @classmethod
    def only_letters_and_digits_check(cls, fields_value: Union[username, password, confirm_password]) -> User:
        if not all(char.isdigit() or char.isalpha() for char in fields_value):
            raise ValueError('Password must contain only letters and numbers!')
        return fields_value


    @model_validator(mode='after')
    @classmethod
    def passwords_match(cls, fields_value: Union[password, confirm_password]) -> User:
        if fields_value.confirm_password != fields_value.password:
            raise ValueError('Passwords do not match.')
        return fields_value


class SUserLogin(BaseModel):
    username: str
    password: str
