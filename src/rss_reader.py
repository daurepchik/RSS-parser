import logging
import sys

from arg_parser import create_arg_parser, check_args, logger as arg_parser_logger
from feed_cacher import cache_feed, print_cached_feed, logger as feed_cacher_logger
from rss_parser import parse_rss_feed, print_feed, logger as rss_parser_logger
from settings import LOGGER_LEVEL, SHRUG_EMOJI

main_logger = logging.getLogger('RSSReader')
main_logger.setLevel(LOGGER_LEVEL)
logger_handler = logging.StreamHandler(sys.stdout)
logger_handler.setLevel(LOGGER_LEVEL)
logger_formatter = logging.Formatter('%(asctime)s - "%(name)s" - %(levelname)s: %(message)s')
logger_handler.setFormatter(logger_formatter)
main_logger.addHandler(logger_handler)

_loggers = [main_logger, arg_parser_logger, feed_cacher_logger, rss_parser_logger]


def main():
    """
    The Main function that controls all the program's flow
    """
    args = create_arg_parser()
    for logger in _loggers:
        logger.disabled = args.verbose
    main_logger.info('Program started')
    try:
        check_args(args)
        if not args.date:
            feed = parse_rss_feed(args.URL, args.limit)
            print_feed(feed, args.json)
            cache_feed(args.URL, feed)
        else:
            print_cached_feed(args.date, args.URL, args.limit, args.json)
    except Exception:
        if args.verbose:
            # TODO: remove raise line
            raise
            sys.exit(f'Error occurred {SHRUG_EMOJI}. Try again with "--verbose" option for more information')
        else:
            sys.exit()
    main_logger.info('Program end')


if __name__ == '__main__':
    main()
"""
- https://news.yahoo.com/rss
- https://lifehacker.com/rss
- https://moxie.foxnews.com/feedburner/world.xml
- http://rss.cnn.com/rss/edition.rss
- https://rss.nytimes.com/services/xml/rss/nyt/World.xml
- http://feeds.bbci.co.uk/news/world/rss.xml
- https://www.techrepublic.com/rssfeeds/topic/cloud
"""
