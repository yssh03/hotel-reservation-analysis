import logging
import os
from datetime import datetime

LOG_DIRS = os.path.join(os.getcwd(), "logs")
LOG_FILE = os.path.join(
    LOG_DIRS, f"log_{datetime.now().strftime('%y-%m-%d')}.log")

logging.basicConfig(filename=LOG_FILE,
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    level=logging.INFO)


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger
