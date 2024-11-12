from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    KAKAO_CLIENT_ID: str = "temp_id"
    KAKAO_CLIENT_SECRET: str = "temp_secret"
    REDIRECT_URI: str = "http://localhost:8000/auth/kakao/callback"
    JWT_SECRET: str = "temp_secret"
    JWT_ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"

settings = Settings()