from .base import ElasticBaseModel


class InnerFilmWork(ElasticBaseModel):
    title: str
    imdb_rating: float

    def to_elastic(self) -> dict:
        return {
            'id': str(self.id),
            'title': self.title,
            'imdb_rating': self.imdb_rating,
        }


class Genre(ElasticBaseModel):
    name: str
    description: str = 'Default'
    film_works: list[InnerFilmWork]

    def to_elastic(self) -> dict:
        return {
            'id': str(self.id),
            'name': self.name,
            'description': self.description,
            'movies': [movie.to_elastic() for movie in self.film_works],
        }
