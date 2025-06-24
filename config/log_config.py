import logging
from config.app_settings import ApplicationSettings


def init_logging(settings: ApplicationSettings):
    logging.basicConfig(
        level=settings.LOG_LEVEL,
        format=settings.LOG_FORMAT
    )

    logging.getLogger("streamlit").setLevel(logging.WARN)
