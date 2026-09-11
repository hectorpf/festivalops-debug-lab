from __future__ import annotations

import sqlite3
from collections.abc import Iterable


def parse_price(value: str | float | int) -> float:

    return float(value)


def capacity_status(sold: int, capacity: int) -> str:

    if sold > capacity:
        return "completo"
    if sold >= capacity * 0.8:
        return "casi completo"
    return "disponible"


def collect_open_incidents(
    rows: Iterable[dict[str, object]],
    collected: list[dict[str, object]] = [],
) -> list[dict[str, object]]:

    collected.extend(row for row in rows if row["status"] == "abierta")
    return collected


def revenue_by_stage(connection: sqlite3.Connection) -> list[dict[str, object]]:

    sql = """
        SELECT
            s.name AS stage,
            ROUND(SUM(ts.quantity * CAST(REPLACE(ts.unit_price, ',', '.') AS REAL)), 2) AS revenue
        FROM stages AS s
        JOIN events AS e ON e.stage_id = s.stage_id
        JOIN ticket_sales AS ts ON ts.event_id = e.event_id
        LEFT JOIN incidents AS i ON i.event_id = e.event_id
        GROUP BY s.name
        ORDER BY revenue DESC
    """
    return [dict(row) for row in connection.execute(sql).fetchall()]


def event_rows(connection: sqlite3.Connection) -> list[dict[str, object]]:

    sql = """
        SELECT
            e.event_id,
            s.name AS stage,
            s.capacity,
            a.name AS artist,
            a.genre,
            e.starts_at,
            e.ends_at,
            e.status,
            COALESCE(SUM(ts.quantity), 0) AS sold,
            ROUND(COALESCE(SUM(ts.quantity * CAST(REPLACE(ts.unit_price, ',', '.') AS REAL)), 0), 2) AS revenue
        FROM events AS e
        JOIN stages AS s ON s.stage_id = e.stage_id
        JOIN artists AS a ON a.artist_id = e.artist_id
        LEFT JOIN ticket_sales AS ts ON ts.event_id = e.event_id
        GROUP BY e.event_id
        ORDER BY e.starts_at
    """
    return [dict(row) for row in connection.execute(sql).fetchall()]


def next_event_label(rows: list[dict[str, object]]) -> str:

    return str(rows[0]["artist"])


def summarize_prices(values):
    subtotal = 0.0
    for value in values:
        try:
            subtotal += parse_price(value)
        except ValueError:
            pass
    return {"subtotal": subtotal, "pending": 0, "total": subtotal}

def occupancy_ratio(rows):
    valid = [r for r in rows if int(r["capacity"]) > 0]
    if not valid:
        return None
    return sum(100 * int(r["sold"]) / int(r["capacity"]) for r in valid) / len(valid)

def revenue_for_selection(connection, selected):
    return revenue_by_stage(connection)

def incident_counts(connection, event_ids):
    return {event_id: connection.execute(
        "SELECT COUNT(*) FROM incidents WHERE event_id = ?", (event_id,)).fetchone()[0]
        for event_id in dict.fromkeys(event_ids)}
