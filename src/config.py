from pathlib import Path
from dotenv import load_dotenv
from pydantic import Field, ConfigDict
from pydantic_settings import BaseSettings


BASE_DIR = Path(__file__).resolve().parent
load_dotenv()

class Settings(BaseSettings):
    model_config = ConfigDict(frozen=True)

    UPLOAD_DIR: Path = BASE_DIR / "uploads"
    VECTORSTORE_DIR: Path = BASE_DIR / "vectordb"
    REDIS_URL: str = Field(default="redis://redis:6379", json_schema_extra={"env": "REDIS_URL"})
    OPENAI_API_KEY: str = Field(json_schema_extra={"env": "OPEN_API_KEY"})
    SUPPORTED_FILE_TYPES: tuple[str] = ("pdf",)


    def model_post_init(self, *args) -> None:
        self.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        self.VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)

settings = Settings()