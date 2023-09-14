from datetime import datetime, timedelta
from typing import Any

import common.time_operations as to
from state.storage import BaseStorage

__all__ = (
    'State',
    'ModifiedState',
)


class State:
    """Класс для работы с состояниями."""

    def __init__(self, storage: BaseStorage) -> None:
        self.storage = storage

    def set_state(self, key: str, value: Any) -> None:
        """Установить состояние для определённого ключа."""
        state = self.storage.retrieve_state()
        state[key] = value
        self.storage.save_state(state)

    def get_state(self, key: str) -> Any:
        """Получить состояние по определённому ключу."""
        return self.storage.retrieve_state().get(key)


class ModifiedState(State):
    """Класс для работы с одним полем - дата последнего изменения."""

    def __init__(self, storage: BaseStorage, key: str) -> None:
        self.key = key
        super().__init__(storage)

    def update_last_modified_time(self, new_time: datetime) -> None:
        """Установить новое время последнего изменения."""
        last = self.get_last_modified_time()
        second = timedelta(seconds=1)
        new_time += second
        if not last:
            self.set_state(self.key, to.to_stamp(new_time))
            return

        if new_time.replace(tzinfo=None) > last.replace(tzinfo=None):
            self.set_state(self.key, to.to_stamp(new_time))

    def get_last_modified_time(self) -> datetime | None:
        return to.from_stamp(self.get_state(self.key))
