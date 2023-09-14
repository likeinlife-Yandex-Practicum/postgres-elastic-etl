import abc
import json
from logging import Logger
from typing import Any, Dict

from redis import StrictRedis

__all__ = ('BaseStorage', 'JsonFileStorage', 'RedisStorage')


class BaseStorage(abc.ABC):
    """
    Абстрактное хранилище состояния.

    Позволяет сохранять и получать состояние.
    Способ хранения состояния может варьироваться в зависимости
    от итоговой реализации. Например, можно хранить информацию
    в базе данных или в распределённом файловом хранилище.
    """

    @abc.abstractmethod
    def save_state(self, state: Dict[str, Any]) -> None:
        """Сохранить состояние в хранилище."""

    @abc.abstractmethod
    def retrieve_state(self) -> Dict[str, Any]:
        """Получить состояние из хранилища."""


class JsonFileStorage(BaseStorage):
    """
    Реализация хранилища, использующего локальный файл.

    Формат хранения: JSON
    """

    def __init__(self, logger: Logger, file_path: str) -> None:
        self.file_path = file_path
        self._logger = logger

    def save_state(self, state: Dict[str, Any]) -> None:
        """Сохранить состояние в хранилище."""
        with open(self.file_path, 'w') as file_obj:
            json.dump(state, file_obj, indent=4, ensure_ascii=False)

    def retrieve_state(self) -> Dict[str, Any]:
        """Получить состояние из хранилища."""
        try:
            with open(self.file_path, 'r') as file_obj:
                return json.load(file_obj)
        except (FileNotFoundError, json.JSONDecodeError):
            self._logger.warning('No state file provided. Continue with default file')
            return {}


class RedisStorage(BaseStorage):
    """Реализация хранилища, использующего Redis."""

    def __init__(self, logger: Logger, redis: StrictRedis) -> None:
        self.redis = redis
        self._logger = logger

    def save_state(self, state: Dict) -> None:
        """Сохранить состояние в хранилище."""
        self.redis.hmset('state', state)

    def retrieve_state(self) -> Dict:
        """Получить состояние из хранилища."""
        state = self.redis.hgetall('state')
        if state:
            return state  # type: ignore
        else:
            self._logger.warning('No state provided. Continue with default state')
            return {}
