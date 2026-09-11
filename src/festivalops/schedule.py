from __future__ import annotations

from collections.abc import Iterable


def minute_of_show(starts_at: str) -> int:

    time_part = starts_at.split("T", 1)[1]
    hour, minute = (int(part) for part in time_part[:5].split(":"))
    return hour * 60 + minute


def sort_for_show(rows: Iterable[dict[str, object]]) -> list[dict[str, object]]:

    return sorted(rows, key=lambda row: minute_of_show(str(row["starts_at"])))
