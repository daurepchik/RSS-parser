import logging
import sys

from argument_parser.arg_parser import create_arg_parser, check_args, logger as arg_parser_logger
from feed_cacher.feed_cacher import cache_feed, collect_cached_feeds, print_cached_feeds, logger as feed_cacher_logger
from format_converter.converter import convert_to_html, convert_to_pdf, logger as converter_logger
from rss_parser.rss_parser import parse_rss_feed, print_feed, logger as rss_parser_logger
from settings.settings import LOGGER_LEVEL, SHRUG_EMOJI, logger as settings_logger

main_logger = logging.getLogger('RSSReader')
main_logger.setLevel(LOGGER_LEVEL)
logger_handler = logging.StreamHandler(sys.stdout)
logger_handler.setLevel(LOGGER_LEVEL)
logger_formatter = logging.Formatter('%(asctime)s - "%(name)s" - %(levelname)s: %(message)s')
logger_handler.setFormatter(logger_formatter)
main_logger.addHandler(logger_handler)

_loggers = [main_logger, arg_parser_logger, converter_logger, feed_cacher_logger, rss_parser_logger, settings_logger]


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
        if args.dest_file:
            main_logger.info('Changing files destination folder')
            with open('settings/USER_PATH.py', 'w', encoding='utf-8') as fw:
                dest_file = args.dest_file.replace('\\', '/')
                fw.write(f'USER_PATH = "{dest_file}"')
            main_logger.info(f'OK. Destination folder is changed to {dest_file}')
        if not args.date and args.URL:
            feed = parse_rss_feed(args.URL, args.limit)
            print_feed(feed, args.json)
            cache_feed(args.URL, feed)
            feeds = [feed]
            if args.to_html:
                convert_to_html(feeds)
            if args.to_pdf:
                convert_to_pdf(feeds)
        elif args.date:
            feeds = collect_cached_feeds(args.date, args.URL, args.limit)
            print_cached_feeds(feeds, args.json)
            if args.to_html:
                convert_to_html(feeds)
            if args.to_pdf:
                convert_to_pdf(feeds)

    except Exception:
        if args.verbose:
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
