from pathlib import Path

"""Settings of the program"""
import logging
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL

from settings.USER_PATH import USER_PATH

logger = logging.getLogger('RSSReader.settings')

# Choose one logger level from [DEBUG, INFO, WARNING, ERROR, CRITICAL]. Default - INFO
LOGGER_LEVEL = INFO
# Current Version of the Program
VERSION = 0.4
# Emojis
SHRUG_EMOJI = r'¯\_(ツ)_/¯'

# Setting root path for project's caching and html formatting
ROOT_PATH = Path.home() / 'Desktop' / 'RSS-READER'

if USER_PATH.title() != "None":
    USER_PATH = Path(USER_PATH)
    if USER_PATH.exists():
        ROOT_PATH = USER_PATH / 'RSS-READER'
    else:
        logger.error(f'Something wrong with {USER_PATH}')
        logger.info('Changing files destination folder to Default')
        with open('settings/USER_PATH.py', 'w', encoding='utf-8') as fw:
            fw.write(f'USER_PATH = "None"')
        logger.info(f'OK. Destination folder is changed to {ROOT_PATH}')

if not ROOT_PATH.exists():
    ROOT_PATH.mkdir()
CACHE_DIR_PATH = ROOT_PATH / 'CachedFeeds'
CACHE_FILE_PATH = CACHE_DIR_PATH / 'feeds_cache.json'
CACHE_IMGS_PATH = CACHE_DIR_PATH / 'CachedFeedImages'

FORMAT_TARGET_PATH = ROOT_PATH / 'FormatConverter'
TEMPLATES_LOCATION = Path(__file__).parent.parent / 'format_converter' / 'templates'
