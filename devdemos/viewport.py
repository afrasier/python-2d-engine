import logging

from events import Orchestrator


def dev_viewport():
    logger = logging.getLogger(__name__)

    logger.info("Starting viewport demo")

    # Create our window
    