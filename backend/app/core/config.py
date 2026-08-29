from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Centralized app configuration, loaded from environment variables (or a .env file).
    This replaces the hardcoded `pymysql.connect(...)` call that used to live in
    the old Flask app's __init__.py.
    """

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Postgres connection string, e.g.
    # postgresql+psycopg2://user:password@localhost:5432/flights
    database_url: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/flights"

    # JWT settings
    secret_key: str = "dev-secret-change-me"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24  # 1 day

    # CORS - the React dev server origin
    cors_origins: list[str] = ["http://localhost:5173"]


settings = Settings()
