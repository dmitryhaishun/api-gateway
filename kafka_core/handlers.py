import logging
from typing import Any

from app.celery.celery import app

logger = logging.getLogger(__name__)


@app.task(name="user_registration_handler")
def user_registration_handler(message: Any):
    logger.info(f" message - {message}")
