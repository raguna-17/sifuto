from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.modules.order.model import Order, OrderItem


# =========================================================
# Order（ヘッダー）
# =========================================================

# -------------------------
# 単一取得（注文詳細）
# -------------------------

async def get_order_by_id(db: AsyncSession, order_id: int):
    stmt = select(Order).where(Order.id == order_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


# -------------------------
# ユーザーの注文一覧
# -------------------------

async def get_orders_by_user(db: AsyncSession, user_id: int):
    stmt = (
        select(Order)
        .where(Order.user_id == user_id)
        .order_by(Order.created_at.desc())
    )

    result = await db.execute(stmt)
    return result.scalars().all()


# -------------------------
# 全注文（管理用）
# -------------------------

async def get_all_orders(db: AsyncSession):
    stmt = select(Order).order_by(Order.created_at.desc())
    result = await db.execute(stmt)
    return result.scalars().all()


# -------------------------
# 作成（Orderヘッダー）
# -------------------------

async def add_order(db: AsyncSession, order: Order):
    db.add(order)
    await db.flush()
    return order


# -------------------------
# 削除（Order）
# -------------------------

async def delete_order(db: AsyncSession, order: Order):
    await db.delete(order)
    await db.flush()


# =========================================================
# OrderItem（明細）
# =========================================================

# -------------------------
# 注文に紐づく明細取得
# -------------------------

async def get_items_by_order_id(db: AsyncSession, order_id: int):
    stmt = select(OrderItem).where(OrderItem.order_id == order_id)
    result = await db.execute(stmt)
    return result.scalars().all()


# -------------------------
# 単一取得
# -------------------------

async def get_item_by_id(db: AsyncSession, item_id: int):
    stmt = select(OrderItem).where(OrderItem.id == item_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


# -------------------------
# 単一追加
# -------------------------

async def add_item(db: AsyncSession, item: OrderItem):
    db.add(item)
    await db.flush()
    return item


# -------------------------
# 複数追加（注文作成時）
# -------------------------

async def add_items(db: AsyncSession, items: list[OrderItem]):
    db.add_all(items)
    await db.flush()
    return items


# -------------------------
# 削除
# -------------------------

async def delete_item(db: AsyncSession, item: OrderItem):
    await db.delete(item)
    await db.flush()


# -------------------------
# 注文単位で明細削除（必要時）
# -------------------------

async def delete_items_by_order_id(db: AsyncSession, order_id: int):
    items = await get_items_by_order_id(db, order_id)

    for item in items:
        await db.delete(item)

    await db.flush()