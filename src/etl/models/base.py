import abc
import uuid

from pydantic import BaseModel, Extra


class ElasticBaseModel(BaseModel, abc.ABC):
    """
    BaseModel for ETL.

    Allow to dump to elastic.
    """

    id: uuid.UUID

    @abc.abstractmethod
    def to_elastic(self) -> dict:
        """Dump to elastic."""

    class Config:
        extra = Extra.allow
