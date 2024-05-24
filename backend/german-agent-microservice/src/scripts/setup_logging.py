import logging
from agent_service.core.log import ColoredFormatter


# Use this function to set up logging before running the agent

def setup_logging():
    """
    set ups logging
    """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(ColoredFormatter())
    logger.addHandler(ch)