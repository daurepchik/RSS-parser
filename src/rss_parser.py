import json
import logging
from pathlib import Path
import re
import sys
from urllib.request import urlopen

from bs4 import BeautifulSoup
from dateutil import parser

from exceptions import ArgumentError

logger = logging.getLogger('RSSReader.rss_parser')


def connect_to_url(url):
    """
    Function to check connection to provided url and return http response
    :param url: url of website with feed xml data
    :exception: raises ConnectionError if url is invalid or unreachable
    :return: response object returned from urllib.request.urlopen()
    """
    try:
        logger.info(f'Checking connection to {url}')
        response = urlopen(url)
        status_code = response.getcode()
        if 200 <= status_code < 400:
            logger.info(f'URL is valid. Status code: {status_code}')
        elif 400 <= status_code < 500:
            logger.error(f'URL is invalid. Status code: {status_code}')
            raise ConnectionError(f'URL is invalid. Status code: {status_code}')
        elif 500 <= status_code < 600:
            logger.error(f'Internal Server Error. Status code: {status_code}')
            raise ConnectionError(f'Internal Server Error. Status code: {status_code}')
    except Exception as e:
        logger.error(f'Something went wrong. Error Msg: {e}')
        raise
    logger.info(f'OK. Connection checked')
    return response


def create_soup_parser(content):
    """
    Function checks if provided website contains rss feed and returns soup object if correct
    :param content: content got from http response
    :return: BeautifulSoup object if no errors
    """
    logger.info(f'Checking if website contains RSS feed')
    soup = BeautifulSoup(content, "lxml-xml")
    if not soup.find('rss'):
        logger.error(f'Website does not contain rss feed')
        raise ArgumentError('Website does not contain rss feed')
    logger.info('OK. Website checked. RSS feed found')
    return soup


def parse_rss_feed(url, limit):
    """
    Function that parses RSS feed from the url provided and creates dictionary with the key feed information
    :param url: url of website with feed xml data
    :param limit: integer number of feed items to limit
    :return: dictionary with feed data
    """
    logger.info(f'Parsing RSS feed in {url}')
    response = connect_to_url(url)
    content = response.read()
    soup = create_soup_parser(content)
    feed_items = []
    logger.info('Searching for RSS feed items')
    try:
        for item in soup.find_all('item', limit=limit):
            item_dict = {
                'title': BeautifulSoup(item.title.string, 'lxml').text,
                'date': str(parser.parse(item.pubDate.string)) if item.pubDate else 'Empty',
                'link': item.link.string if item.link else 'Empty',
                'description': BeautifulSoup(item.description.string, 'lxml').text
                                if item.description
                                else 'Empty',
                'img': item.find('media:content')['url'] if item.find('media:content') else 'Empty'
            }
            feed_items.append(item_dict)
        logger.info('OK. RSS feed items found')
        logger.info('Creating RSS feed dictionary')
        feed = {
            'title': soup.title.string,
            'description': BeautifulSoup(soup.description.string, 'lxml').text.strip('\n')
            if soup.description.string
            else 'Empty',
            'link': soup.find('link', text=re.compile(r'\w+')).string,
            'items': feed_items,
        }
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = '/'.join(Path(__file__).parts[-2:])
        logger.error(f'{exc_type.__name__}: {e}. File: {file_name}. Line №: {exc_tb.tb_lineno}. '
                     f'Function: parse_rss_feed(url, limit)')
        raise
    logger.info('OK. RSS feed dictionary created')
    logger.info(f'OK. Parsed RSS feed')
    return feed


def feed_items_to_string(feed_items):
    """
    Function that converts array of feed items to prettified string for output
    :param feed_items: array of RSS feed items
    :return: prettified string from feed items array
    """
    logger.info('Converting feed items array to string for printing')
    items_string = ""
    for i, item in enumerate(feed_items):
        items_string += f"Item {i + 1}:\n"
        for key, value in item.items():
            items_string += f"\t{key.title()}: {value}\n"
        items_string += '\n'
    logger.info('OK. Feed items converted to string')
    return items_string


def feed_to_string(feed):
    """
    Function that converts feed dictionary to prettified string for output
    :param feed: RSS feed as python dictionary
    :return: prettified string from feed dictionary
    """
    logger.info('Converting feed dictionary to prettified string')
    output_text = f"""Feed: {feed['title']}
Description: {feed['description']}
Feed Link: {feed['link']}

{feed_items_to_string(feed['items'])}"""
    logger.info('OK. Feed converted to string')
    return output_text


def print_feed(feed, as_json):
    """
    Function that prints parsed RSS feed to console
    :param feed: dictionary with parsed RSS feed to be printed
    :param as_json: boolean parameter to define output as json or not
    :return: dictionary with feed information
    """
    output_text = feed_to_string(feed)
    try:
        if as_json:
            logger.info('Printing RSS feed as JSON')
            print(json.dumps(feed, indent=2, sort_keys=False))
        else:
            logger.info('Printing RSS feed as usual')
            print(output_text)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = '/'.join(Path(__file__).parts[-2:])
        logger.error(f'{exc_type.__name__}: {e}. File: {file_name}. Line №: {exc_tb.tb_lineno}. '
                     f'Function: print_feed')
        raise
    logger.info(f'OK. RSS feed printed')
