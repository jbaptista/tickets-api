"""Module to provide slqalchemy adapters for the repository pattern."""

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


def make_session_factory(url: str, *args, **kwargs) -> async_sessionmaker:
    """Async session factory."""
    db_engine = create_async_engine(url, *args, **kwargs)
    return async_sessionmaker(bind=db_engine, expire_on_commit=False)


class SqlAlchemyRepositoryMixin:
    """Mixin class to enable the use of SQLAlchemy in a repository pattern.

    To use this mixin, just use the session method to get a new session within
    a context manager.
    Example:
    > async with self.session() as session:
    >    session.execute(...)
    >    session.commit()

    """

    def __init__(self, session_factory: async_sessionmaker):
        # Create a session factory
        self.session = session_factory  # async_sessionmaker(bind=self._engine, expire_on_commit=False)
