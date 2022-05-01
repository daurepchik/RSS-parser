import argparse
import logging
from pathlib import Path
import re

from exceptions.custom_exceptions import ArgumentError
from  settings.settings import VERSION

logger = logging.getLogger('RSSReader.arg_parser')


def create_arg_parser():
    """
    Function that initializes program's Argument Parser with the parameters, which you can see by running the
    program as cli command with the [--help|-h] argument
    :return: Namespace object with the provided arguments
    """
    parser = argparse.ArgumentParser(
        prog="RSS Parser",
        description="Pure Python command-line RSS reader"
    )
    parser.add_argument('URL', nargs='?', default=False, help='RSS URL')
    parser.add_argument('--version', '-V', action='version', version=f'{parser.prog}: {VERSION}',
                        help='print version info')
    parser.add_argument('--json', '-j', action='store_true', help='print result as JSON in stdout')
    parser.add_argument('--verbose', '-v', action='store_false', help='outputs verbose status messages')
    parser.add_argument('--limit', '-l', type=int, help='limit news topics if this parameter provided')
    parser.add_argument('--date', '-d', help='get news from cache. Date format: YYYYMMDD')
    parser.add_argument('--to-html', action='store_true', help='convert fetched RSS feed to HTML format')
    parser.add_argument('--to-pdf', action='store_true', help='convert fetched RSS feed to PDF format')
    parser.add_argument('--dest-file', '-f',
                        help='configure path to store caching and converted HTML and PDF files. Default - None')
    return parser.parse_args()


def check_args(args):
    """
    Function to check correctness of provided arguments to Argument Parser
    :param args: Namespace object with the provided arguments
    :exception: Raises ArgumentError exception if "limit" argument is less than 1
    :exception: Raises ArgumentError exception if "URL" is not provided
    :exception: Raises ArgumentError exception if "date" argument is not in the correct format
    """
    logger.info('Checking Argument Parser arguments')
    if args.limit is not None and int(args.limit) < 1:
        logger.error('"limit" argument is less than 1. Should be greater than or equal to 1')
        raise ArgumentError('"limit" argument is less than 1')
    if not args.URL and not args.date and not args.dest_file:
        logger.error('The required argument "URL" is missing')
        raise ArgumentError('The required argument "URL" is missing')
    if args.date and not re.compile(r'\d{8}').fullmatch(args.date):
        logger.error('The "date" argument is not in the correct format')
        raise ArgumentError('The "date" argument is not in the correct format')
    if args.dest_file and not Path(args.dest_file).exists() and not args.dest_file == 'None':
        logger.error('Incorrect folder path. Try putting the path in quotes')
        raise ArgumentError()
    elif args.dest_file and not Path(args.dest_file).is_dir() and not args.dest_file == 'None':
        logger.error('Incorrect folder type')
        raise ArgumentError()
    logger.info('OK. Argument Parser arguments was checked')
