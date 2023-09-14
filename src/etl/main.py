import time
from datetime import datetime
from typing import Generator

import elasticsearch as els
from common import backoff, logger
from config import elastic_config, mainloop_config, redis_config
from enums import DBTable, ESIndex, RedisKey
from etl_pipelines import etl_save as etl
from etl_pipelines import fetch_changed
from etl_pipelines import film_pipeline as fp
from etl_pipelines import genre_pipeline as gp
from psycopg2.extensions import connection
from redis import StrictRedis
from service_connection import get_postgres_session
from state import state, storage


def filmwork_etl_fetchers(
    _session: connection,
    _state: state.ModifiedState,
    _els: els.Elasticsearch,
) -> tuple[Generator[None, datetime, None], ...]:
    """
    Configure all nodes links.

    Procedure: fetch changes -> get film -> save film
    Returns: tuple of fetchers generators.
    """
    save_to_etl = etl.save_to_es(_els, ESIndex.FILMWORK)

    transformer = fp.transform_filmworks(save_to_etl)  # make Pydantic model from fetched results

    film_fetcher = fp.get_filmwork_by_id(_session, transformer)  # get all film info, including persons and genres

    film_by_person = fp.get_filmwork_ids_by_persons(_session, film_fetcher)

    film_by_genre = fp.get_filmwork_ids_by_genres(_session, film_fetcher)

    person_change_fetcher = fetch_changed(
        DBTable.PERSON,
        _session,
        _state,
        film_by_person,
    )
    genre_change_fetcher = fetch_changed(
        DBTable.GENRE,
        _session,
        _state,
        film_by_genre,
    )

    film_change_fetcher = fetch_changed(
        DBTable.FILMWORK,
        _session,
        _state,
        film_fetcher,
    )

    return (
        film_change_fetcher,
        person_change_fetcher,
        genre_change_fetcher,
    )


def genre_etl_fetchers(
    _session: connection,
    _state: state.ModifiedState,
    _els: els.Elasticsearch,
) -> tuple[Generator[None, datetime, None], ...]:
    """
    Configure all nodes links.

    Procedure: fetch changes -> get film -> save film
    Returns: tuple of fetchers generators.
    """
    save_to_etl = etl.save_to_es(_els, ESIndex.GENRE)

    transformer = gp.transform_genres(save_to_etl)  # make Pydantic model from fetched results

    genre_fetcher = gp.get_genres(_session, transformer)  # get all film info, including persons and genres

    genre_change_fetcher = fetch_changed(
        DBTable.GENRE,
        _session,
        _state,
        genre_fetcher,
    )

    return (genre_change_fetcher,)


def run_fetchers(last_modified: datetime | None, fetchers: tuple[Generator[None, datetime, None], ...]):
    if last_modified is None:
        fetchers[0].send(datetime.min)
    else:
        for fetcher in fetchers:
            fetcher.send(last_modified)


def main():
    _logger = logger.get_logger(__name__)

    @backoff()
    def inside():
        while True:
            with get_postgres_session() as _session:
                _redis = StrictRedis(**redis_config.model_dump())
                _film_state = state.ModifiedState(
                    storage.RedisStorage(_logger, _redis),
                    RedisKey.FILMWORK.value,
                )
                _genre_state = state.ModifiedState(
                    storage.RedisStorage(_logger, _redis),
                    RedisKey.GENRE.value,
                )
                _els = els.Elasticsearch(elastic_config.get_hosts())

                while True:
                    film_fetchers = filmwork_etl_fetchers(
                        _session,  # type: ignore
                        _film_state,
                        _els,
                    )

                    genre_fetchers = genre_etl_fetchers(
                        _session,  # type: ignore
                        _genre_state,
                        _els,
                    )

                    run_fetchers(_film_state.get_last_modified_time(), film_fetchers)
                    run_fetchers(_genre_state.get_last_modified_time(), genre_fetchers)

                    _logger.info('Another iteration')
                    time.sleep(mainloop_config.retry_time)

    inside()


if __name__ == '__main__':
    main()
