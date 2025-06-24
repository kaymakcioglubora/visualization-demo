import logging
from config.app_settings import ApplicationSettings
from influxdb_client import InfluxDBClient


_log = logging.getLogger(__name__)

_client: InfluxDBClient | None = None


def init_db(settings: ApplicationSettings):
    """
    Load database settings from the environment variables
    """

    db_settings = {k: v for k, v in settings.dict().items() if k.startswith('DB_')}

    _log.info("Loading database settings")
    _log.debug(f"Loaded settings: {db_settings}")
    _log.debug(f"Database org: {settings.DB_ORG}")

    global _client

    if not _client:
        _client = InfluxDBClient(
            url=settings.DB_URL,
            token=settings.DB_TOKEN,
            org=settings.DB_ORG
        )

    if _client.ping():
        _log.info("Successfully connected to DB")
    else:
        _log.error(f"Error connecting to DB using db settings: {db_settings}")
        # raise Exception(f"Error connecting to DB using db settings: {db_settings}")

    return _client


async def close_db():
    """
    Close the database connection
    """
    _log.info("Closing database connection")
    if _client:
        _client.close()
    _log.info("Database connection closed")
