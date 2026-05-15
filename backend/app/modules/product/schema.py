from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


# --- 共通フィールド ---
class ProductBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=5000)

    price: int = Field(ge=0)
    stock: int = Field(ge=0)

    image_url: str | None = Field(default=None, max_length=500)
    is_active: bool = True


# --- 作成 ---
class ProductCreate(ProductBase):
    pass


# --- 更新（部分更新専用）---
class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=5000)

    price: int | None = Field(default=None, ge=0)
    stock: int | None = Field(default=None, ge=0)

    image_url: str | None = Field(default=None, max_length=500)
    is_active: bool | None = None


# --- レスポンス（DB出力専用DTO）---
class ProductRead(BaseModel):
    id: int

    name: str
    description: str | None

    price: int
    stock: int
    image_url: str | None
    is_active: bool

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)