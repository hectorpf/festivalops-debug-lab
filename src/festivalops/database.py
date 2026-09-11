from __future__ import annotations

import sqlite3
from contextlib import closing
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATABASE_PATH = PROJECT_ROOT / "data" / "generated" / "festivalops.sqlite"
SOURCE_SQL = PROJECT_ROOT / "data" / "source" / "festival.sql"


def ensure_database(path: Path = DATABASE_PATH) -> Path:
    """Crea la base local cuando todavía no existe."""

    if path.exists():
        return path
    path.parent.mkdir(parents=True, exist_ok=True)
    with closing(sqlite3.connect(path)) as connection:
        connection.executescript(SOURCE_SQL.read_text(encoding="utf-8"))
    return path


def connect_database(path: Path = DATABASE_PATH) -> sqlite3.Connection:
    """Abre la base con filas accesibles por nombre de columna."""

    ensure_database(path)
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def memory_database() -> sqlite3.Connection:
    """Crea una copia efimera de la fuente para ejemplos y pruebas."""

    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    connection.executescript(SOURCE_SQL.read_text(encoding="utf-8"))
    return connection


def integrity_report(connection: sqlite3.Connection) -> dict[str, object]:
    """Devuelve comprobaciones pequeñas y fáciles de mostrar en clase."""

    return {
        "integrity": connection.execute("PRAGMA integrity_check").fetchone()[0],
        "foreign_key_errors": connection.execute("PRAGMA foreign_key_check").fetchall(),
        "events": connection.execute("SELECT COUNT(*) FROM events").fetchone()[0],
    }
