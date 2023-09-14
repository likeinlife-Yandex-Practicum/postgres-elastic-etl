from .base import ElasticBaseModel


class Person(ElasticBaseModel):
    name: str

    def to_elastic(self) -> dict:
        return {
            'id': str(self.id),
            'name': self.name,
        }
