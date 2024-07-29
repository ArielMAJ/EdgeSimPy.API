"""
Application's and its environment's configuration.
"""

import os

from sqlalchemy import URL, AsyncAdaptedQueuePool, NullPool


class DatabaseConfig:
    """Database configuration."""

    DATABASE_DRIVERNAME = os.getenv("DATABASE_DRIVERNAME", "postgresql+asyncpg")
    POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE", "postgres")
    POSTGRES_URI = (
        f"{DATABASE_DRIVERNAME}:"
        f"//{POSTGRES_USER}:{POSTGRES_PASSWORD}"
        f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"
    )
    DB_URL = URL(
        drivername=DATABASE_DRIVERNAME,
        username=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        database=POSTGRES_DATABASE,
        query={},
    )
    POSTGRES_ECHO = os.getenv("POSTGRES_ECHO", "false").lower() == "true"
    POOL_PRE_PING = os.getenv("POOL_PRE_PING", True)
    POOL_SIZE = int(os.getenv("POOL_SIZE", 5))
    MAX_OVERFLOW = int(os.getenv("MAX_OVERFLOW", 10))

    DATABASE_ENABLE_CONNECTION_POOLING = (
        os.getenv("DATABASE_ENABLE_CONNECTION_POOLING", "true").lower() == "true"
    )

    _POOLING_ARGS = (
        {
            "poolclass": AsyncAdaptedQueuePool,
            "pool_size": POOL_SIZE,
            "max_overflow": MAX_OVERFLOW,
        }
        if DATABASE_ENABLE_CONNECTION_POOLING
        else {
            "poolclass": NullPool,
        }
    )

    ENGINE_ARGS = {
        "echo": POSTGRES_ECHO,
        "pool_pre_ping": POOL_PRE_PING,
        **_POOLING_ARGS,
    }


class AuthConfig:
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


class Config:
    """Base configuration."""

    ENVIRONMENT = os.getenv("ENVIRONMENT", "DEV")
    DEBUG = ENVIRONMENT == "DEV"
    TESTING = ENVIRONMENT == "TEST"

    HOST = os.getenv("APPLICATION_HOST", "127.0.0.1")
    PORT = int(os.getenv("APPLICATION_PORT", "3000"))
    WORKERS_COUNT = int(os.getenv("WORKERS_COUNT", "1"))
    RELOAD = os.getenv("RELOAD", "true").lower() == "true"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    APPLICATION_ROOT = os.getenv("APPLICATION_ROOT", "")

    DATABASE: DatabaseConfig = DatabaseConfig()
    AUTH: AuthConfig = AuthConfig()


class TestConfig(Config):
    """Test configuration."""

    ENVIRONMENT = "test"
    TESTING = True
    DEBUG = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False
