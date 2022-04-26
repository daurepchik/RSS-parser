import hashlib
import json
import logging
import sys
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlretrieve

from dateutil.parser import parse, ParserError

from rss_parser import print_feed
from settings import SHRUG_EMOJI

_FILE_PATH = Path(__file__).parent.parent
_CACHE_FILE_PATH = _FILE_PATH / 'CachedFeeds' / 'feeds_cache.json'
_CACHE_IMGS_PATH = _FILE_PATH / 'CachedFeeds' / 'CachedFeedImages'
logger = logging.getLogger('RSSReader.feed_cacher')


def _open_cached_feed():
    """
    Function to open cached json file with news if exists, and convert it to python dictionary. Else create new
    dictionary
    :return: dictionary with existing news if so. Else empty
    """
    logger.info('Opening cached views')
    news_cache = {}
    if _CACHE_FILE_PATH.exists():
        with open(_CACHE_FILE_PATH) as fr:
            news_cache = json.load(fr)
    logger.info('OK. Cached views opened')
    return news_cache


def cache_feed(url, feed):
    """
    Function to cache RSS feed in local machine in json format
    :param url: url of RSS feed
    :param feed: dictionary created after parsing RSS feed
    :return: writes cached rss feed to file
    """
    feeds_cache = _open_cached_feed()
    netloc = urlparse(url).netloc
    logger.info(f'Caching feed into {_CACHE_FILE_PATH.name}')
    logger.info('Putting data into dictionary with correct format for caching')
    try:
        feeds_cache[netloc] = feeds_cache.get(netloc, {})

        items_hashes = set(feeds_cache[netloc].get('items_hashes', set()))
        dates = feeds_cache[netloc].get('dates', {})
        for item in feed['items']:
            item_hash = hashlib.md5(bytes(item['title'], 'UTF-8')).hexdigest()
            if item['img'] != 'Empty':
                logger.info('Caching item\'s image into images folder')
                urlretrieve(item['img'], _CACHE_IMGS_PATH / f'{item_hash}.jpg')
                logger.info('OK. Item\'s Image cached')
            logger.info('Checking if feed item is already cached')
            if item_hash not in items_hashes:
                try:
                    logger.info('Getting date from feed item')
                    date = parse(item['date']).strftime('%Y%m%d')
                except (ParserError, TypeError):
                    logger.error('Something wrong with feed item\'s date')
                    date = 'None'
                logger.info('Separating feed item by date')
                dates[date] = dates.get(date, [])
                dates[date].append(item)
            logger.info('Adding feed item to cache dictionary')
            items_hashes.add(item_hash)

        feeds_cache[netloc].update({key: value for key, value in feed.items() if key != 'items'})
        feeds_cache[netloc]['items_hashes'] = list(items_hashes)
        feeds_cache[netloc]['dates'] = dates
        logger.info('OK. Dictionary for feed caching is created')
        logger.info('Writing dictionary into file')
        with open(_CACHE_FILE_PATH, 'w') as fw:
            json.dump(feeds_cache, fw, indent=2, sort_keys=False)
        logger.info('OK. File with Cached feed is created')
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = '/'.join(Path(__file__).parts[-2:])
        logger.error(f'{exc_type.__name__}: {e}. File: {file_name}. Line №: {exc_tb.tb_lineno}. '
                     f'Function: cache_feed')
        raise
    logger.info('OK. Cache json file is created')


def print_cached_feed(date, url, limit, as_json):
    """
    Function to output cached feed to stdout
    :param date: date from which the data should be displayed
    :param url: url of the source from which the data was cached
    :param limit: the number of items to be printed
    :param as_json: define in which format to print the result, json or string
    :return: prints the output
    """
    news_cache = _open_cached_feed()
    if len(news_cache) == 0:
        logger.info('Feed cache is not created yet')
        print(f'No output? Check the logs then {SHRUG_EMOJI}')
        return
    try:
        item_counter = 0
        for netloc, cached_feed in filter(lambda x: x[0] == urlparse(url).netloc if url else x[0], news_cache.items()):
            logger.info(f'Printing cashed feed from "{netloc}"')
            if date in cached_feed['dates']:
                item_date, items = list(filter(lambda x: x[0] == date, cached_feed['dates'].items()))[0]
                feed = {
                    'title': cached_feed['title'],
                    'description': cached_feed['description'],
                    'link': cached_feed['link'],
                    'items': items[:limit]
                }
                print_feed(feed, as_json)
                logger.info(f'OK. Cached RSS feed is printed')
                item_counter += 1
            else:
                logger.warning(f'Not found items for "{netloc}" on provided date')
        if not item_counter:
            print(f'No items? Check the logs then {SHRUG_EMOJI}')
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = '/'.join(Path(__file__).parts[-2:])
        logger.error(f'{exc_type.__name__}: {e}. File: {file_name}. Line №: {exc_tb.tb_lineno}. '
                     f'Function: print_cached_feed')
        raise
