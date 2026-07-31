import functools
from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    host: str = "127.0.0.1"
    port: int = 8000
    log_level: str = "info"
    reload: bool = False
    db_url: str = f"sqlite+aiosqlite:///{Path.home() / '.cellmetpro' / 'data.db'}"
    upload_dir: str = str(Path.home() / ".cellmetpro" / "uploads")


@functools.lru_cache
def get_settings() -> Settings:
    return Settings()
