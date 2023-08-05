import logging
import sys

__version__ = "0.2.1"

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))

GOLDENMASK = "__goldenmask__"
GOLDENMASK_INFO = ".goldenmask"
