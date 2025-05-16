from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, computed_field

class Settings(BaseSettings):
    DB_USERNAME: str = ""
    DB_PASSWORD: str = ""
    DB_HOSTNAME: str = ""
    DB_PORT: int = 0
    DB_NAME: str = ""
    WORKER_GRPC_URL: str = "task_worker:50051"

    @computed_field
    def database_url(self) -> str:
        return (f"postgresql+asyncpg://{self.DB_USERNAME}:{self.DB_PASSWORD}@"
                f"{self.DB_HOSTNAME}:{self.DB_PORT}/{self.DB_NAME}")

    class Config:
        env_file = ".env"

settings = Settings()
print("database_url", settings.database_url, flush=True)
