from datetime import datetime

from sqlalchemy import String, Text, Integer, Boolean, CheckConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Product(Base):
    __tablename__ = "products"

    __table_args__ = (
        CheckConstraint("price >= 0", name="check_price_non_negative"),
        CheckConstraint("stock >= 0", name="check_stock_non_negative"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    name: Mapped[str] = mapped_column(String(55), nullable=False)

    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    price: Mapped[int] = mapped_column(Integer, nullable=False)

    stock: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # -------------------------
    # relationships
    # -------------------------

    cart_items: Mapped[list["CartItem"]] = relationship(
        "CartItem",
        back_populates="product",
    )

    order_items: Mapped[list["OrderItem"]] = relationship(
        "OrderItem",
        back_populates="product",
    )