import argparse
import logging
import sys

from settings import (
    DB_PSQL,
    DB_USER_PSQL,
    DB_PASS_PSQL,
    DB_HOST_PSQL,
    DB_PORT_PSQL,
    MONITORING_SERVICE_HOST,
    MONITORING_SERVICE_PORT,
)

from analyze_service.analyzer import handle_raw_data
from monitoring_service.utils import get_request

logger = logging.getLogger('trello_creator')


def set_up_logger():
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(logging.Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
    logger.addHandler(handler)


def parse_args():
    parser = argparse.ArgumentParser(description='Input commands like "http/database" "seed(int)"')
    parser.add_argument(
        'source', choices=[ArgChoices.HTTP.value], help='Where will the information comes from',
    )
    parser.add_argument('seed', type=int, help='random generator seed')
    args = parser.parse_args()
    return args.source, args.seed, args.price


def main(data_source, seed):
    logger.info('Trello creator starts...')
    analyzed_data = None
    base_url = f'http://{MONITORING_SERVICE_HOST}:{MONITORING_SERVICE_PORT}'

    if data_source == ArgChoices.HTTP.value:
        endpoint = 'monitoring/infrastructure/using/summary'
        url = f'{base_url}/{endpoint}/{seed}'
        raw_data = get_request(url=url)
        analyzed_data = handle_raw_data(raw_data)


if __name__ == '__main__':
    set_up_logger()
    data_source, seed, price = parse_args()
    main(data_source, seed, price)
