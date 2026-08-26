import logging
import os

LOG_FOLDER = "logs"

if not os.path.exists(LOG_FOLDER):  # pragma: no cover
    os.makedirs(LOG_FOLDER)  # pragma: no cover


logging.basicConfig(  # pragma: no cover
    filename="logs/billing_system.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)
