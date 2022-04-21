import logging
import sys

from arg_parser import create_arg_parser, check_args, logger as arg_parser_logger
from rss_parser import print_feed, logger as rss_parser_logger

main_logger = logging.getLogger('RSSReader')
main_logger.setLevel(logging.INFO)
logger_handler = logging.StreamHandler(sys.stdout)
logger_handler.setLevel(logging.INFO)
logger_formatter = logging.Formatter('%(asctime)s - "%(name)s" - %(levelname)s: %(message)s')
logger_handler.setFormatter(logger_formatter)
main_logger.addHandler(logger_handler)

loggers = [main_logger, arg_parser_logger, rss_parser_logger]


def main():
    """
    The Main function that controls all the program's flow
    """
    args = create_arg_parser()
    for logger in loggers:
        logger.disabled = args.verbose
    main_logger.info('Program started')
    try:
        check_args(args)
        print_feed(args.URL, args.limit, args.json)
    except Exception:
        sys.exit(f'Error occurred. Check logs')
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
