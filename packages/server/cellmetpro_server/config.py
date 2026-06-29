import functools

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    host: str = "127.0.0.1"
    port: int = 8000
    log_level: str = "info"
    reload: bool = False


@functools.lru_cache
def get_settings() -> Settings:
    return Settings()
