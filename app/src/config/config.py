import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Класс настроек проекта, считывающий данные из переменных окружения."""

    model_config = SettingsConfigDict(
        env_file=os.path.join('src', 'config', '.env'),
        env_file_encoding='UTF-8',
        extra='allow',
    )

    # Настройки базы данных.
    DB_HOST: str = 'it_start_pg_database'
    DB_PORT: int = 5432
    POSTGRES_DB: str = 'test_db'
    POSTGRES_PASSWORD: str = 'db_pass'
    POSTGRES_USER: str = 'db_user'

    REDIS_HOST: str = 'it_start_redis'
    REDIS_PORT: int = 6379

    # Настройки безопасности.
    DOMAIN_IP: str = '127.0.0.1'
    DOMAIN_NAME: str = 'localhost'

    # Настройки сервиса.
    ASGI_PORT: int = 80
    DEBUG: bool = False
    WORKERS_AMOUNT: int = 4


settings = Settings()
