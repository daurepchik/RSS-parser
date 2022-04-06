import argparse
import re
from pprint import pprint

from urllib.request import urlopen
from bs4 import BeautifulSoup


def rss_reader(site, limit=None):
    response = urlopen(site)
    xml = response.read()
    soup = BeautifulSoup(xml, "lxml-xml")

    feed_items = []
    for item in soup.find_all('item', limit=limit):
        item_dict = {
            'title': item.title.string,
            'date': item.pubDate.string,
        }
        if item.link:
            item_dict['link'] = item.link.string
        if item.description:
            item_dict['description'] = BeautifulSoup(item.description.string, 'lxml').text
        feed_items.append(item_dict)

    feed = {
        'title': soup.title.string,
        'description': BeautifulSoup(soup.description.string, 'lxml').text.strip('\n'),
        'link': soup.find('link', text=re.compile(r'\w+')).string,
        'items': feed_items,
    }
    return feed


def feed_items_to_string(feed_items):
    item_string = ""
    for i, item in enumerate(feed_items):
        item_string += f"Item {i + 1}:\n"
        for key, value in item.items():
            item_string += f"\t{key.title()}: {value}\n"
        item_string += '\n'
    return item_string


def print_feed(site, limit=None, as_json=False):
    feed = rss_reader(site, limit)
    if as_json:
        pprint(feed, sort_dicts=False)
    else:
        output_text = f"""Feed: {feed['title']}
Description: {feed['description']}
Feed Link: {feed['link']}

{feed_items_to_string(feed['items'])}"""
        print(output_text)


if __name__ == '__main__':
    print_feed("https://news.yahoo.com/rss", 1)
    # print_feed("https://feeds.simplecast.com/54nAGcIl", 1)
    # print_feed("https://rss.art19.com/apology-line", 1)

# parser = argparse.ArgumentParser(description='Videos to images')
# parser.add_argument('indir', type=str,
#                     help='Input dir for videos')
# parser.add_argument('outdir', type=str,
#                     help='Output dir for image')
# args = parser.parse_args()
