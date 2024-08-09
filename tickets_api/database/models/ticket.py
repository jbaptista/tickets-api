from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from tickets_api.schemas.ticket import Severity
from sqlalchemy import ForeignKey


class Ticket(Base):
    __tablename__ = "tickets"

    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column(nullable=True)
    severity: Mapped[Severity] = mapped_column()
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    subcategory_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
