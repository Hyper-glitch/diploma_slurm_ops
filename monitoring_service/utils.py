"""Module that help get data with http."""
import logging

import requests

logger = logging.getLogger('trello_creator')


def get_request(url):
    logger.info('Get data from http server.')
    resources = requests.get(url=url)
    resources.raise_for_status()
    logger.info('Data successfully got from http server.')
    return resources.text
