from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str
    JWT_SIGNING_ALGORITHM: str

    class Config:
        env_file = '.env'


settings = Settings()
