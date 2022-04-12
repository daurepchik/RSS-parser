import argparse
import logging

from exceptions import ArgumentError
import settings

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
    parser.add_argument('URL', help='RSS URL')
    parser.add_argument('--version', '-V', action='version', version=f'{parser.prog}: {settings.VERSION}',
                        help='print version info')
    parser.add_argument('--json', '-j', action='store_true', help='print result as JSON in stdout')
    parser.add_argument('--verbose', '-v', action='store_false', help='outputs verbose status messages')
    parser.add_argument('--limit', '-l', type=int, help='limit news topics if this parameter provided')
    return parser.parse_args()


def check_args(args):
    """
    Function to check correctness of provided arguments to Argument Parser
    :param args: Namespace object with the provided arguments
    :exception: Raises ArgumentError exception if limit argument is less than 1
    """
    logger.info('Checking Argument Parser arguments')
    if args.limit is not None and int(args.limit) < 1:
        logger.error('"limit" argument is less than 1. Should be greater than or equal to 1')
        raise ArgumentError('"limit" argument is less than 1')
    logger.info('OK. Argument Parser arguments was checked')
