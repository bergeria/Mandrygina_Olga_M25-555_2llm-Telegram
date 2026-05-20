"""
Базовый декларативный класс SQLAlchemy.

Все ORM-модели должны наследоваться от Base.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
