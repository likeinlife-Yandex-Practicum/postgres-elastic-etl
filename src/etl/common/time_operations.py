from datetime import datetime

from common.errors import IncorrectTimeError


def to_stamp(time: datetime) -> float:
    return time.timestamp()


def from_stamp(time: float | bytes | str | None) -> datetime | None:

    if isinstance(time, float):
        return datetime.fromtimestamp(time)
    elif isinstance(time, bytes | str):
        return datetime.fromtimestamp(float(time))
    elif time is None:
        return None
    else:
        raise IncorrectTimeError(time)
