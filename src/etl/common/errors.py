from typing import Any


class WrongRoleError(Exception):
    """Role mismatched: director, writer, actor."""

    def __init__(self, role: Any, *args: object) -> None:
        msg = f'Incorrect role: {role}'
        super().__init__(msg, *args)


class IncorrectTimeError(Exception):
    """Got Incorrect time."""

    def __init__(self, time: Any, *args: object) -> None:
        msg = f'Incorrect time: {time}'
        super().__init__(msg, *args)
