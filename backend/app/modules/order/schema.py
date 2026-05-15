from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

from app.core.enums import OrderStatus


# -------------------------
# OrderItem
# -------------------------

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int = Field(ge=1)


class OrderItemResponse(OrderItemBase):
    id: int
    price_at_purchase: int

    model_config = ConfigDict(from_attributes=True)


# -------------------------
# Order
# -------------------------

class OrderCreate(BaseModel):
    # カート or 複数商品前提
    items: list[OrderItemBase] = Field(min_length=1)


class OrderUpdate(BaseModel):
    status: OrderStatus


class OrderResponse(BaseModel):
    id: int
    user_id: int
    status: OrderStatus
    total_price: int
    created_at: datetime

    items: list[OrderItemResponse]

    model_config = ConfigDict(from_attributes=True)