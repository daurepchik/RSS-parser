from pathlib import Path

"""Settings of the program"""
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL

# Choose one logger level from [DEBUG, INFO, WARNING, ERROR, CRITICAL]. Default - INFO
LOGGER_LEVEL = INFO
# Current Version of the Program
VERSION = 3.1
# Emojis
SHRUG_EMOJI = r'¯\_(ツ)_/¯'

CACHE_DIR_PATH = Path(__file__).parent.parent.parent / 'CachedFeeds'
CACHE_FILE_PATH = CACHE_DIR_PATH / 'feeds_cache.json'
CACHE_IMGS_PATH = CACHE_DIR_PATH / 'CachedFeedImages'

FORMAT_TARGET_PATH = Path(__file__).parent.parent.parent / 'FormatConverter'
TEMPLATES_LOCATION = Path(__file__).parent.parent / 'format_converter' / 'templates'
