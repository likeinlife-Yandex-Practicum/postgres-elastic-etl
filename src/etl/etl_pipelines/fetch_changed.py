from datetime import datetime
from typing import Generator

import common.logger as _logger
from common.coroutine import coroutine
from enums.db_table import DBTable
from psycopg2.extensions import connection
from psycopg2.extras import DictCursor
from state.state import ModifiedState

logger = _logger.get_logger(__name__)


@coroutine
def fetch_changed(
    table: DBTable,
    session: connection,
    state: ModifiedState,
    next_node: Generator,
) -> Generator[None, datetime, None]:
    """
    Fetch rows, where `modified` column older than sended datetime.

    Also set uncommited last modified date to state
    """
    while last_updated := (yield):
        cursor: DictCursor = session.cursor()  # type: ignore
        logger.info(f'Fetching content.{table.value} changed after {last_updated}')
        sql = f'SELECT * FROM content.{table.value} WHERE modified > %s order by modified asc'
        cursor.execute(sql, (last_updated,))
        while results := cursor.fetchmany(size=100):
            next_node.send(results)
            state.update_last_modified_time(results[-1].get('modified'))
