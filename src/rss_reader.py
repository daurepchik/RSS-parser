import logging
import sys

from arg_parser import create_arg_parser, check_args
from rss_parser import print_feed

logger = logging.getLogger('RSSReader')
logger.setLevel(logging.INFO)
logger_handler = logging.StreamHandler(sys.stdout)
logger_handler.setLevel(logging.INFO)
logger_formatter = logging.Formatter('%(asctime)s - "%(name)s" - %(levelname)s: %(message)s')
logger_handler.setFormatter(logger_formatter)
logger.addHandler(logger_handler)


def main():
    """
    The Main function that controls all the program's flow
    """
    args = create_arg_parser()
    logger.disabled = args.verbose
    check_args(args)
    print_feed(args.URL, args.limit, args.json)


if __name__ == '__main__':
    logger.info('Program started')
    main()  # https://news.yahoo.com/rss/
    logger.info('Program end')
