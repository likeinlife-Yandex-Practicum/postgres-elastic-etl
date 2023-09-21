from typing import Generator

from common import coroutine, get_logger
from psycopg2.extensions import connection

logger = get_logger(__name__)


@coroutine
def get_persons(session: connection, next_node: Generator) -> Generator[None, list[dict], None]:
    """Get persons info."""
    while genre_dicts := (yield):
        cursor = session.cursor()
        logger.info('Fetching persons')
        _ids = tuple([genre.get('id') for genre in genre_dicts])
        sql = '''SELECT
                p.id,
                p.full_name as name,
                JSON_AGG(
                    DISTINCT jsonb_build_object(
                        'id', fw.id,
                        'title', fw.title,
                        'imdb_rating', fw.rating,
                        'roles', (SELECT json_agg(in_pfw.role)
                                FROM content.person_film_work in_pfw
                                where p.id = in_pfw.person_id AND fw.id = in_pfw.film_work_id)
                    )
                ) as movies
                FROM content.person p
                JOIN content.person_film_work pfw ON p.id = pfw.person_id
                JOIN content.film_work fw ON pfw.film_work_id = fw.id
                WHERE p.id IN %s
                GROUP BY p.id;'''
        cursor.execute(sql, (_ids,))

        while results := cursor.fetchmany(size=100):
            next_node.send(results)
