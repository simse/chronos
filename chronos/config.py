# TODO: Find another place for this line
import os

from loguru import logger


CHRONOS = os.getenv("CHRONOS_PATH")

if CHRONOS is None:
    logger.critical("Enviroment variable CHRONOS_PATH not set, aborting program")
    logger.info("The CHRONOS_PATH variable must contain the Chronos metadata folder.")
    exit()