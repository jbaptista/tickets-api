from datetime import datetime

from sqlalchemy import BigInteger
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, MappedAsDataclass
from sqlalchemy.sql import func
from sqlalchemy.dialects import sqlite

# enable tests to run with sqlite
BigIntegerType = BigInteger()
BigIntegerType = BigIntegerType.with_variant(sqlite.INTEGER(), "sqlite")


class Base(MappedAsDataclass, DeclarativeBase):
    """Base class for all models. It provides a default id, created_at and updated_at.
    Usage:
    > class Person(Base):
    >   __tablename__ = "people"
    >  name: Mapped[str] = mapped_column()
    >  age: Mapped[int] = mapped_column()
    """

    id: Mapped[int] = mapped_column(
        BigIntegerType, primary_key=True, autoincrement=True, init=False
    )
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), init=False)
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now(), init=False
    )
