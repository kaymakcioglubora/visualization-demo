from pydantic_settings import BaseSettings


class ApplicationSettings(BaseSettings):
    """
    Application settings
    """
    APP_NAME: str = "NET Visualization Framework"
    APP_VERSION: str = "0.0.1"
    APP_DESCRIPTION: str = "Visualization Framework Demo for Internal Use"
    ENVIRONMENT: str = "default"

    LOG_LEVEL: str = "DEBUG"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    DB_URL: str = "localhost"
    DB_TOKEN: str = "token"
    DB_ORG: str = "org"
