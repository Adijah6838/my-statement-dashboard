import os
from pydantic_settings import BaseSettings, SettingsConfigDict

# Build absolute path to the backend directory
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../../"))
ENV_FILE = os.path.join(BASE_DIR, ".env")

# Safety check: Verify the file actually exists before Pydantic tries to load it
if not os.path.exists(ENV_FILE):
    raise FileNotFoundError(
        f"\n\n❌ ERROR: Could not find the .env file.\n"
        f"Expected location: {ENV_FILE}\n"
        f"Please make sure you created the '.env' file inside the 'backend' folder.\n"
    )

class Settings(BaseSettings):
    PROJECT_NAME: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    DATABASE_URL: str

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()