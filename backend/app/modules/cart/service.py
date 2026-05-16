from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload

from app.modules.cart.model import Cart, CartItem


# -------------------------
# カート取得（中身込み）
# -------------------------
async def get_cart(db: AsyncSession, user_id: int):
    stmt = (
        select(Cart)
        .where(Cart.user_id == user_id)
        .options(selectinload(Cart.items).selectinload(CartItem.product))
    )

    result = await db.execute(stmt)
    return result.scalar_one_or_none()


# -------------------------
# カートアイテム一覧
# -------------------------
async def get_cart_items(db: AsyncSession, user_id: int):
    cart = await get_cart(db, user_id)
    if not cart:
        return []
    return cart.items


# -------------------------
# カート作成
# -------------------------
async def create_cart(db: AsyncSession, user_id: int):
    cart = Cart(user_id=user_id)
    db.add(cart)
    await db.flush()
    return cart


# -------------------------
# カートアイテム取得
# -------------------------
async def get_cart_item(db: AsyncSession, cart_id: int, product_id: int):
    stmt = select(CartItem).where(
        CartItem.cart_id == cart_id,
        CartItem.product_id == product_id,
    )

    result = await db.execute(stmt)
    return result.scalar_one_or_none()


# -------------------------
# 追加
# -------------------------
async def add_to_cart(db: AsyncSession, user_id: int, product_id: int, quantity: int):
    cart = await get_cart(db, user_id)

    if not cart:
        cart = await create_cart(db, user_id)

    item = await get_cart_item(db, cart.id, product_id)

    if item:
        item.quantity += quantity
        result = item
    else:
        result = CartItem(
            cart_id=cart.id,
            product_id=product_id,
            quantity=quantity,
        )
        db.add(result)

    await db.commit()
    await db.refresh(result)
    return result


# -------------------------
# 更新
# -------------------------
async def update_cart_item(db: AsyncSession, user_id: int, product_id: int, quantity: int):
    cart = await get_cart(db, user_id)
    if not cart:
        return None

    item = await get_cart_item(db, cart.id, product_id)
    if not item:
        return None

    item.quantity = quantity

    await db.commit()
    await db.refresh(item)
    return item


# -------------------------
# 削除
# -------------------------
async def remove_from_cart(db: AsyncSession, user_id: int, product_id: int):
    cart = await get_cart(db, user_id)
    if not cart:
        return False

    item = await get_cart_item(db, cart.id, product_id)
    if not item:
        return False

    await db.delete(item)
    await db.commit()
    return True


# -------------------------
# 全削除
# -------------------------
async def clear_cart(db: AsyncSession, user_id: int):
    cart = await get_cart(db, user_id)
    if not cart:
        return True

    stmt = delete(CartItem).where(CartItem.cart_id == cart.id)
    await db.execute(stmt)

    await db.commit()
    return True