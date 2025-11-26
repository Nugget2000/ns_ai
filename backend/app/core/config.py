import os

class Settings:
    PROJECT_NAME: str = "NS AI Backend"
    VERSION: str = "0.1.2"
    DESCRIPTION: str = "Backend for NS AI application"
    ENABLE_CLOUD_LOGGING: bool = os.getenv("ENABLE_CLOUD_LOGGING", "True").lower() == "true"

settings = Settings()
