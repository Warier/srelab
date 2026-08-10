import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    database_url: str = os.getenv(
        "SCALEPASS_DATABASE_URL",
        "sqlite:///./scalepass.db",
    )
    secret_key: str = os.getenv(
        "SCALEPASS_SECRET_KEY",
        "scalepass-local-development-secret",
    )


settings = Settings()
