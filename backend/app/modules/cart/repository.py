from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload

from app.modules.cart.model import Cart, CartItem


# -------------------------
# カート取得（ユーザー単位）
# -------------------------

async def get_cart_by_user(db: AsyncSession, user_id: int):
    stmt = (
        select(Cart)
        .where(Cart.user_id == user_id)
        .options(
            selectinload(Cart.items).selectinload(CartItem.product)
        )
    )

    result = await db.execute(stmt)
    return result.scalar_one_or_none()


# -------------------------
# カート作成
# -------------------------

async def create_cart(db: AsyncSession, user_id: int):
    cart = Cart(user_id=user_id)
    db.add(cart)
    await db.flush()
    return cart


# -------------------------
# カートアイテム取得（単一）
# -------------------------

async def get_cart_item(db: AsyncSession, cart_id: int, product_id: int):
    stmt = (
        select(CartItem)
        .where(
            CartItem.cart_id == cart_id,
            CartItem.product_id == product_id,
        )
    )

    result = await db.execute(stmt)
    return result.scalar_one_or_none()


# -------------------------
# カートアイテム作成
# -------------------------

async def create_cart_item(db: AsyncSession, cart_item: CartItem):
    db.add(cart_item)
    await db.flush()
    return cart_item


# -------------------------
# カートアイテム更新（数量のみ）
# -------------------------

async def update_cart_item_quantity(db: AsyncSession, cart_item: CartItem, quantity: int):
    cart_item.quantity = quantity
    await db.flush()
    return cart_item


# -------------------------
# カートアイテム削除
# -------------------------

async def delete_cart_item(db: AsyncSession, cart_item: CartItem):
    await db.delete(cart_item)
    await db.flush()


# -------------------------
# カート全削除（中身だけ）
# -------------------------

async def clear_cart_items(db: AsyncSession, cart_id: int):
    stmt = delete(CartItem).where(CartItem.cart_id == cart_id)
    await db.execute(stmt)
    await db.flush()