import hashlib
import logging
import sys
from pathlib import Path
import uuid

import jinja2.exceptions
from jinja2 import Environment, FileSystemLoader
from xhtml2pdf import pisa

from settings.settings import CACHE_DIR_PATH, CACHE_IMGS_PATH, FORMAT_TARGET_PATH, TEMPLATES_LOCATION

logger = logging.getLogger('RSSReader.converter')


def get_cached_image(item):
    """
    Jinja custom template filter to get images for item that were cached from rss feed
    :param item: RSS feed item
    :return: path to item's cached image
    """
    item_hash = hashlib.md5(bytes(item['title'], 'UTF-8')).hexdigest()
    image_path = f'../{CACHE_DIR_PATH.name}/{CACHE_IMGS_PATH.name}/{item_hash}.jpg'
    return image_path


def setup_jinja():
    """
    Function to setup Jinja html templatizer
    :return: Jinja template object
    """
    logger.debug('Creating Jinja Environment')
    environment = Environment(loader=FileSystemLoader(TEMPLATES_LOCATION))
    environment.filters["get_cached_image"] = get_cached_image
    html_template = environment.get_template('html_template.html')
    logger.debug('OK. Jinja Environment created')
    return html_template


def convert_to_html(feeds):
    """
    Function that accepts list of RSS feed,
    formats information to html file
    :param feeds: array of feed
    """
    try:
        logger.info('Creating RSS feed in HTML format')
        html_file_name = f"rss_feed_{str(uuid.uuid4())[:6]}.html"
        target_path = FORMAT_TARGET_PATH / html_file_name
        logger.info(f'Writing file to {target_path}')
        template = setup_jinja()
        with open(target_path, 'w+', encoding='utf-8') as file:
            file.write(template.render(feeds=feeds))
        logger.info('OK. HTML file created')
    except TypeError:
        logger.error("Not valid path or input data.")
        raise
    except jinja2.exceptions.TemplateNotFound:
        logger.error("Something happened to HTML template")
        raise


def convert_to_pdf(feeds):
    """
    Function that accepts list of RSS feed,
    formats information to html text,
    then converts everything into pdf file
    :param feeds: array of feed
    """
    try:
        logger.info('Creating RSS feed in PDF format')
        pdf_file_name = f"rss_feed_{str(uuid.uuid4())[0:6]}.pdf"
        target_path = FORMAT_TARGET_PATH / pdf_file_name
        logger.info(f'Writing file to {target_path}')
        template = setup_jinja()
        source_html_text = template.render(feeds=feeds)
        with open(target_path, "w+b") as target:
            pisa.CreatePDF(source_html_text, dest=target, encoding='utf-8')
        logger.info('OK. PDF file created')
    except FileNotFoundError:
        logger.error('Something happened to destination folder')
        raise
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = '/'.join(Path(__file__).parts[-2:])
        logger.error(f'{exc_type.__name__}: {e}. File: {file_name}. Line №: {exc_tb.tb_lineno}. '
                     f'Function: convert_to_pdf')
        raise
