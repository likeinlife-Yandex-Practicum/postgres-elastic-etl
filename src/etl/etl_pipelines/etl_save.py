from typing import Generator

import elasticsearch as els
from common import coroutine, get_logger
from elasticsearch.helpers import bulk
from enums import ESIndex
from models import ElasticBaseModel

logger = get_logger(__name__)


@coroutine
def save_to_es(
    _els: els.Elasticsearch,
    _index: ESIndex,
) -> Generator[None, list[ElasticBaseModel], None]:
    _index_name = _index.value
    while es_obj_list := (yield):
        logger.info(f'Received for saving {len(es_obj_list)} to index {_index_name}')

        actions = [{'_index': _index_name, '_id': es_obj.id, '_source': es_obj.to_elastic()} for es_obj in es_obj_list]

        bulk_responses = bulk(_els, actions, stats_only=True)

        logger.info(f'Successfully saved {bulk_responses[0]}')

        if bulk_responses[1]:
            logger.warning(f'Couldnt save {bulk_responses[1]}')
