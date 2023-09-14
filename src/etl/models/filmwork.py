from datetime import datetime
from typing import Any

import common.errors as errors
from enums.person_role import PersonRole

from .base import ElasticBaseModel


class FilmWork(ElasticBaseModel):
    title: str
    description: str
    creation_date: datetime | str | None
    file_path: str | None
    rating: float
    type: str

    persons: list[dict]
    genres: list[str]

    def model_post_init(self, __context: Any) -> None:
        self.actors: list[dict] = []
        self.directors: list[str] = []
        self.writers: list[dict] = []

        for person in self.persons:
            match person.get('role'):
                case PersonRole.ACTOR.value:
                    self.actors.append({'id': person['id'], 'name': person['name']})
                case PersonRole.DIRECTOR.value:
                    self.directors.append(person['name'])
                case PersonRole.WRITER.value:
                    self.writers.append({'id': person['id'], 'name': person['name']})
                case _:
                    raise errors.WrongRoleError(person)

        self.actors_names = [actor.get('name') for actor in self.actors]
        self.writers_names = [writer.get('name') for writer in self.writers]

    def to_elastic(self) -> dict:
        return {
            'id': str(self.id),
            'title': self.title,
            'description': self.description,
            'imdb_rating': self.rating,
            'genre': self.genres,
            'director': self.directors,
            'actors_names': self.actors_names,
            'writers_names': self.writers_names,
            'actors': self.actors,
            'writers': self.writers,
        }
