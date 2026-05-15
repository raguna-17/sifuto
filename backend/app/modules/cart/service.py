from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.cart import repository as cart_repo
from app.modules.cart.model import Cart, CartItem

async def get_cart(db: AsyncSession, user_id: int):
    cart = await cart_repo.get_cart_by_user(db, user_id)

    if not cart:
        return None

    return cart

async def add_to_cart(
    db: AsyncSession,
    user_id: int,
    product_id: int,
    quantity: int,
):
    # 1. カート取得 or 作成
    cart = await cart_repo.get_cart_by_user(db, user_id)

    if not cart:
        cart = await cart_repo.create_cart(db, user_id)

    # 2. 既存アイテム確認
    item = await cart_repo.get_cart_item(db, cart.id, product_id)

    if item:
        # 3. 既存なら数量加算
        new_qty = item.quantity + quantity
        result = await cart_repo.update_cart_item_quantity(db, item, new_qty)
    else:
        # 4. 新規追加
        new_item = CartItem(
            cart_id=cart.id,
            product_id=product_id,
            quantity=quantity,
        )
        result = await cart_repo.create_cart_item(db, new_item)

    # 5. 永続化
    await db.commit()
    await db.refresh(result)

    return result

async def update_cart(
    db: AsyncSession,
    user_id: int,
    product_id: int,
    quantity: int,
):
    # 1. カート取得
    cart = await cart_repo.get_cart_by_user(db, user_id)

    if not cart:
        return None

    # 2. アイテム取得
    item = await cart_repo.get_cart_item(db, cart.id, product_id)

    if not item:
        return None

    # 3. 更新
    result = await cart_repo.update_cart_item_quantity(db, item, quantity)

    # 4. commit
    await db.commit()
    await db.refresh(result)

    return result

async def remove_from_cart(
    db: AsyncSession,
    user_id: int,
    product_id: int,
):
    # 1. カート取得
    cart = await cart_repo.get_cart_by_user(db, user_id)

    if not cart:
        return False

    # 2. アイテム取得
    item = await cart_repo.get_cart_item(db, cart.id, product_id)

    if not item:
        return False

    # 3. 削除
    await cart_repo.delete_cart_item(db, item)

    # 4. commit
    await db.commit()

    return True

async def clear_cart(db: AsyncSession, user_id: int):
    # 1. カート取得
    cart = await cart_repo.get_cart_by_user(db, user_id)

    if not cart:
        return True

    # 2. アイテム全削除
    await cart_repo.clear_cart_items(db, cart.id)

    # 3. commit
    await db.commit()

    return True