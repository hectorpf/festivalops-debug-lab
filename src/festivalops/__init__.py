"""Lógica del laboratorio educativo FestivalOps."""

from .database import connect_database, ensure_database

__all__ = ["connect_database", "ensure_database"]
