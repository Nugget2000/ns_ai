from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "NS AI Backend"
    VERSION: str = "0.1"
    DESCRIPTION: str = "Backend for NS AI application"
    GOOGLE_APPLICATION_CREDENTIALS: str | None = None
    

settings = Settings()
