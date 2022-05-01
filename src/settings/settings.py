from pathlib import Path

"""Settings of the program"""
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL

# Choose one logger level from [DEBUG, INFO, WARNING, ERROR, CRITICAL]. Default - INFO
LOGGER_LEVEL = INFO
# Current Version of the Program
VERSION = 0.4
# Emojis
SHRUG_EMOJI = r'¯\_(ツ)_/¯'

# Setting root path for project's caching and html formatting
ROOT_PATH = Path.home() / 'Desktop' / 'RSS-READER'

# SETUP YOUR PATH HERE
USER_PATH = None
# END SETUP YOUR PATH

if USER_PATH:
    USER_PATH = Path(USER_PATH)
    if USER_PATH.exists() and USER_PATH.is_dir():
        ROOT_PATH = USER_PATH / 'RSS-READER'
    elif not USER_PATH.exists():
        exit('Incorrect folder path.\nExiting')
    elif not USER_PATH.is_dir():
        exit('Incorrect folder type.\nExiting')

if not ROOT_PATH.exists():
    ROOT_PATH.mkdir()
CACHE_DIR_PATH = ROOT_PATH / 'CachedFeeds'
CACHE_FILE_PATH = CACHE_DIR_PATH / 'feeds_cache.json'
CACHE_IMGS_PATH = CACHE_DIR_PATH / 'CachedFeedImages'

FORMAT_TARGET_PATH = ROOT_PATH / 'FormatConverter'
TEMPLATES_LOCATION = Path(__file__).parent.parent / 'format_converter' / 'templates'
