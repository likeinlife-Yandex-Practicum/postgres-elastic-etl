from typing import Generator

from common import coroutine, get_logger
from psycopg2.extensions import connection

logger = get_logger(__name__)


@coroutine
def get_filmwork_ids_by_persons(session: connection, next_node: Generator) -> Generator[None, list[dict], None]:
    while person_dicts := (yield):
        cursor = session.cursor()
        logger.info('Fetching movies with persons')
        _ids = tuple([person.get('id') for person in person_dicts])
        sql = '''SELECT DISTINCT fw.id
                FROM content.film_work fw
                JOIN content.person_film_work pfw ON fw.id = pfw.film_work_id
                JOIN content.person p ON pfw.person_id = p.id
                WHERE p.id IN %s;'''
        cursor.execute(sql, (_ids,))

        while results := cursor.fetchmany(size=100):
            next_node.send(results)


@coroutine
def get_filmwork_ids_by_genres(session: connection, next_node: Generator) -> Generator[None, list[dict], None]:
    while genre_dicts := (yield):
        cursor = session.cursor()
        logger.info('Fetching movies with genres')
        _ids = tuple([genre.get('id') for genre in genre_dicts])
        sql = '''SELECT fw.id
                FROM content.film_work fw
                JOIN content.genre_film_work gfw ON fw.id = gfw.film_work_id
                JOIN content.genre g ON gfw.genre_id = g.id
                WHERE g.id IN %s;'''
        cursor.execute(sql, (_ids,))

        while results := cursor.fetchmany(size=100):
            next_node.send(results)


@coroutine
def get_filmwork_by_id(session: connection, next_node: Generator) -> Generator[None, list[dict], None]:
    while film_work_ids := (yield):
        cursor = session.cursor()
        logger.info('Fetching movies')
        _ids = tuple([film_work.get('id') for film_work in film_work_ids])
        sql = '''SELECT
                fw.id,
                fw.title,
                fw.description,
                fw.creation_date,
                fw.file_path,
                fw.rating,
                fw.type,
                fw.created,
                fw.modified,
                COALESCE (
                    json_agg(
                        DISTINCT jsonb_build_object(
                            'role', pfw.role,
                            'id', p.id,
                            'name', p.full_name
                        )
                    ) FILTER (WHERE p.id is not null),
                    '[]'
                ) as persons,
                json_agg(
                    DISTINCT jsonb_build_object(
                        'id', g.id,
                        'name', g.name
                    )
                ) as genres
                FROM content.film_work fw
                LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
                LEFT JOIN content.person p ON p.id = pfw.person_id
                LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
                LEFT JOIN content.genre g ON g.id = gfw.genre_id
                WHERE fw.id in %s
                GROUP BY fw.id
                ORDER BY fw.modified;'''

        cursor.execute(sql, (_ids,))

        while results := cursor.fetchmany(size=100):
            next_node.send(results)
