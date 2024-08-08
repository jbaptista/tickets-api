from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from tickets_api.schemas.ticket import Severity


class Ticket(Base):
    __tablename__ = "tickets"

    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column(nullable=True)
    severity: Mapped[Severity] = mapped_column()
