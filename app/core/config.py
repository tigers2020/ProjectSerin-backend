from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    allowed_origins: str
    host: str
    port: int
    class Config:
        env_file = ".env"


settings = Settings()
