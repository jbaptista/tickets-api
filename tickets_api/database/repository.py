"""Module to provide slqalchemy adapters for the repository pattern."""

from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine


def make_db_engine(url: str, *args, **kwargs) -> AsyncEngine:
    """Async engine factory."""
    return create_async_engine(url, *args, **kwargs)


class SqlAlchemyRepositoryMixin:
    """Mixin class to enable the use of SQLAlchemy in a repository pattern.

    To use this mixin, just use the session method to get a new session within
    a context manager.
    Example:
    > async with self.session() as session:
    >    session.execute(...)
    >    session.commit()

    """

    def __init__(self, db_engine: AsyncEngine):
        self._engine = db_engine
        # Create a session factory
        self.session = async_sessionmaker(bind=self._engine, expire_on_commit=False)
