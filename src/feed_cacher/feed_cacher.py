import hashlib
import json
import logging
import sys
from pathlib import Path
import threading
from urllib.parse import urlparse
from urllib.request import urlretrieve
from urllib.error import HTTPError, URLError, ContentTooShortError

from dateutil.parser import parse, ParserError

from rss_parser.rss_parser import print_feed
from settings.settings import SHRUG_EMOJI, CACHE_DIR_PATH, CACHE_FILE_PATH, CACHE_IMGS_PATH

logger = logging.getLogger('RSSReader.feed_cacher')


def open_cached_feed():
    """
    Function to open cached json file with news if exists, and convert it to python dictionary. Else create new
    dictionary
    :return: dictionary with existing news if so. Else empty
    """
    logger.info('Opening cached views')
    news_cache = {}
    if CACHE_FILE_PATH.exists():
        with open(CACHE_FILE_PATH) as fr:
            news_cache = json.load(fr)
    logger.info('OK. Cached views opened')
    return news_cache


def cache_image(item, item_hash):
    """
    Function to collect all item's images and store them in on folder.
    Image's name are hashed title of an item
    :param item_hash: item's title hash
    :param item: RSS feed item dictionary
    :return: stores images in one folder
    """
    if item['img'] != 'Empty':
        if not CACHE_DIR_PATH.exists():
            logger.info('Creating directory for cached news')
            CACHE_DIR_PATH.mkdir()
            CACHE_IMGS_PATH.mkdir()
            logger.info('OK. Directory created')
        try:
            urlretrieve(item['img'], CACHE_IMGS_PATH / f'{item_hash}.jpg')
        except (URLError, HTTPError, ContentTooShortError):
            logger.error(f'Something went wrong with image downloading. Image\'s url: \"{item["img"]}\"')
            raise
    else: 
        logger.warning(f'No image for \"{item["title"]}\"')


def cache_feed(url, feed):
    """
    Function to cache RSS feed in local machine in json format
    :param url: url of RSS feed
    :param feed: dictionary created after parsing RSS feed
    :return: writes cached rss feed to file
    """
    feeds_cache = open_cached_feed()
    netloc = urlparse(url).netloc
    logger.info(f'Caching feed into {CACHE_FILE_PATH.name}')
    logger.info('Putting data into dictionary with correct format for caching')
    try:
        feeds_cache[netloc] = feeds_cache.get(netloc, {})

        items_hashes = set(feeds_cache[netloc].get('items_hashes', set()))
        dates = feeds_cache[netloc].get('dates', {})
        image_threads = []
        logger.info('Caching items\' images')
        for item in feed['items']:
            item_hash = hashlib.md5(bytes(item['title'], 'UTF-8')).hexdigest()
            logger.info(f'Checking if feed item \"{item["title"]}\" is already cached')
            if item_hash not in items_hashes:
                logger.info(f'Making preparation of item \"{item["title"]}\" to be cached')
                t = threading.Thread(target=cache_image, args=(item, item_hash))
                t.start()
                image_threads.append(t)
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
            else:
                logger.info(f'\"{item["title"]}\" is already cached')
        if len(image_threads) != 0:
            logger.info('Waiting for images to download')
            for image_thread in image_threads:
                image_thread.join()
            logger.info('OK. Images downloaded')
        feeds_cache[netloc].update({key: value for key, value in feed.items() if key != 'items'})
        feeds_cache[netloc]['items_hashes'] = list(items_hashes)
        feeds_cache[netloc]['dates'] = dates
        logger.info('OK. Dictionary for feed caching is created')
        logger.info('Writing dictionary into file')
        with open(CACHE_FILE_PATH, 'w') as fw:
            json.dump(feeds_cache, fw, indent=2, sort_keys=False)
        logger.info('OK. File with Cached feed is created')
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = '/'.join(Path(__file__).parts[-2:])
        logger.error(f'{exc_type.__name__}: {e}. File: {file_name}. Line №: {exc_tb.tb_lineno}. '
                     f'Function: cache_feed')
        raise


def collect_cached_feeds(date, url, limit):
    """
    Function to read cached RSS feed from json file
    :param date: date from which the data should be displayed
    :param url: url of the source from which the data was cached
    :param limit: the number of items to be printed
    :return: dictionary with rss feeds from different sources
    """
    logger.info("Collection cashed feeds")
    feeds_cache = open_cached_feed()
    if len(feeds_cache) == 0:
        logger.info('Feed cache is not created yet')
        print(f'No output? Check the logs then {SHRUG_EMOJI}')
        return
    try:
        feeds = []
        logger.info('Filtering cached feeds by source')
        filtered_feeds = filter(lambda x: x[0] == urlparse(url).netloc if url else x[0], feeds_cache.items())
        logger.info('OK. Cached feeds are filtered')
        for netloc, cached_feed in filtered_feeds:
            if date in cached_feed['dates']:
                logger.info('Filtering cached feed items by date')
                filtered_feed_items = filter(lambda x: x[0] == date, cached_feed['dates'].items())
                logger.info('OK. Cached feed items are filtered')
                item_date, items = list(filtered_feed_items)[0]
                feed = {
                    'title': cached_feed['title'],
                    'description': cached_feed['description'],
                    'link': cached_feed['link'],
                    'items': items[:limit]
                }
                feeds.append(feed)
            else:
                logger.warning(f'Not found items for "{netloc}" on provided date')
        if feeds:
            logger.info('OK. Cached feed are collected')
            return feeds
        else:
            print(f'No items? Check the logs then {SHRUG_EMOJI}')
            return None
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = '/'.join(Path(__file__).parts[-2:])
        logger.error(f'{exc_type.__name__}: {e}. File: {file_name}. Line №: {exc_tb.tb_lineno}. '
                     f'Function: collect_cached_feeds')
        raise


def print_cached_feeds(feeds, as_json):
    """
    Function to output cached feed to stdout
    :param feeds: array with feed dictionaries
    :param as_json: boolean parameter to define output as json or not
    """
    if feeds:
        for feed in feeds:
            logger.info(f'Printing cashed feed for "{feed["title"]}"')
            print_feed(feed, as_json)
        logger.info(f'OK. Cached RSS feed is printed')



