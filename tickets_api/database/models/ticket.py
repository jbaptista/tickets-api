from enum import Enum

from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Severity(Enum):
    ISSUE_HIGH = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4


class Ticket(Base):
    __tablename__ = "tickets"

    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column(nullable=True)
    severity: Mapped[Severity] = mapped_column()
