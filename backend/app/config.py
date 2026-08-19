from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql://ti_hunt_user:ti_hunt_pass@localhost:5432/ti_hunt"
    redis_url: str = "redis://localhost:6379/0"
    siem_trust_threshold: float = 0.60
    cors_origins: str = "http://localhost:5173"

    class Config:
        env_file = ".env"

settings = Settings()