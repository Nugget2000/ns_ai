import os

class Settings:
    PROJECT_NAME: str = "NS AI Backend"
    VERSION: str = "0.4.1"
    DESCRIPTION: str = "Backend for NS AI application"
    ENABLE_CLOUD_LOGGING: bool = os.getenv("ENABLE_CLOUD_LOGGING", "True").lower() == "true"
    GCP_PROJECT_ID: str = os.getenv("GCP_PROJECT_ID", "")
    CACHE_ENABLED: bool = os.getenv("CACHE_ENABLED", "True").lower() == "true"
    NIGHTSCOUT_URL: str = os.getenv("NIGHTSCOUT_SITE", "")
    NIGHTSCOUT_API_TOKEN: str = os.getenv("NIGHTSCOUT_TOKEN", "")

settings = Settings()
