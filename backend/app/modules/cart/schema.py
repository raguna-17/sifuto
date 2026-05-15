from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


# -------------------------
# 共通
# -------------------------

class CartItemBase(BaseModel):
    product_id: int
    quantity: int = Field(ge=1, default=1)


# -------------------------
# 作成
# -------------------------

class CartItemCreate(CartItemBase):
    pass


# -------------------------
# 更新
# -------------------------

class CartItemUpdate(BaseModel):
    quantity: int = Field(ge=1)


# -------------------------
# レスポンス用
# -------------------------

class CartItemResponse(BaseModel):
    id: int
    cart_id: int
    product_id: int
    quantity: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)