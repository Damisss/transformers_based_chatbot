import logging

#from scania_truck.utils import config
from intent_recognition.utils import helper


#VERSION_PATH = config.PACKAGE_ROOT / 'VERSION'

# Configure logger for use in package
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(helper.get_console_handler())
logger.propagate = False
