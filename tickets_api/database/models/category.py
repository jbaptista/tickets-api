from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class Category(Base):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    active: Mapped[bool] = mapped_column()
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id"), nullable=True
    )

    sub_categories: Mapped[list["Category"]] = relationship(
        "Category", lazy="joined", join_depth=2, init=False
    )
