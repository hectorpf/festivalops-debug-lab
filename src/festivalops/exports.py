from __future__ import annotations

from collections.abc import Iterable


FIELDS = ("event_id", "stage", "artist", "starts_at", "sold", "revenue")


def export_csv(rows: Iterable[dict[str, object]]) -> str:

    lines = [",".join(FIELDS)]
    for row in rows:
        lines.append(",".join(str(row[field]) for field in FIELDS))
    return "\n".join(lines) + "\n"
