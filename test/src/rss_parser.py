import json
import logging
from pathlib import Path
import re
import sys
from urllib.request import urlopen

from bs4 import BeautifulSoup
import inflect

from exceptions import ArgumentError

logger = logging.getLogger('RSSReader.rss_parser')
p = inflect.engine()


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
            item_dict = {'title': BeautifulSoup(item.title.string, 'lxml').text}
            if item.pubDate:
                item_dict['date'] = item.pubDate.string
            if item.link:
                item_dict['link'] = item.link.string
            if item.description:
                item_dict['description'] = BeautifulSoup(item.description.string, 'lxml').text
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
        file_name = Path(__file__).parent.name
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
    :return: prettified string of feed items array
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


def print_feed(url, limit, as_json):
    """
    Function that prints parsed RSS feed to console
    :param url: url of website with feed xml data
    :param limit: integer number of feed items to limit
    :param as_json: boolean parameter to define output as json or not
    :return: prints output to console
    """
    feed = parse_rss_feed(url, limit)
    output_text = f"""Feed: {feed['title']}
Description: {feed['description']}
Feed Link: {feed['link']}

{feed_items_to_string(feed['items'])}"""
    logger.info(f'Printing RSS feed in {url}, limited to {limit} {p.plural("item", limit)}')
    if as_json:
        logger.info('Printing RSS feed as JSON')
        print(json.dumps(feed, indent=2, sort_keys=False))
    else:
        logger.info('Printing RSS feed as usual')
        print(output_text)
    logger.info(f'OK. RSS feed printed')
