from __future__ import annotations

from collections.abc import Iterable


def normalize_stage(value: str) -> str:

    return value.lower().replace(" ", "-")


def filter_by_stage(rows: Iterable[dict[str, object]], requested: str) -> list[dict[str, object]]:

    target = normalize_stage(requested)
    return [row for row in rows if normalize_stage(str(row["stage"])) == target]
