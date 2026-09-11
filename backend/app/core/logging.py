import logging
import sys
from app.core.config import settings


def setup_logging() -> logging.Logger:
    """
    Configure application-wide structured logging for BizMind AI.
    """
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
        force=True,
    )

    return logging.getLogger("BizMindAI")


logger = setup_logging()
