from contextlib import closing, contextmanager

import psycopg2
from common.backoff import backoff
from config import db_config
from psycopg2.extras import DictCursor

__all__ = ('get_postgres_session',)


@backoff()
@contextmanager
def get_postgres_session():
    dsn = {
        'dbname': db_config.name,
        'user': db_config.user,
        'password': db_config.password,
        'host': db_config.host,
        'port': db_config.port,
        'options': '-c search_path=public,content',
    }

    with closing(psycopg2.connect(**dsn, cursor_factory=DictCursor)) as conn:  # type: ignore
        yield conn
