from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload

from app.modules.order.model import Order, OrderItem


# =========================================================
# Order
# =========================================================

async def get_order_by_id(db: AsyncSession, order_id: int):
    stmt = (
        select(Order)
        .options(selectinload(Order.items))
        .where(Order.id == order_id)
    )

    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_orders_by_user(db: AsyncSession, user_id: int):
    stmt = (
        select(Order)
        .options(selectinload(Order.items))
        .where(Order.user_id == user_id)
        .order_by(Order.created_at.desc())
    )

    result = await db.execute(stmt)
    return result.scalars().all()


async def get_all_orders(db: AsyncSession):
    stmt = (
        select(Order)
        .options(selectinload(Order.items))
        .order_by(Order.created_at.desc())
    )

    result = await db.execute(stmt)
    return result.scalars().all()


async def add_order(db: AsyncSession, order: Order):
    db.add(order)
    await db.flush()
    return order


async def delete_order(db: AsyncSession, order: Order):
    await db.delete(order)


# =========================================================
# OrderItem
# =========================================================

async def get_items_by_order_id(db: AsyncSession, order_id: int):
    stmt = select(OrderItem).where(OrderItem.order_id == order_id)

    result = await db.execute(stmt)
    return result.scalars().all()


async def get_item_by_id(db: AsyncSession, item_id: int):
    stmt = select(OrderItem).where(OrderItem.id == item_id)

    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def add_items(db: AsyncSession, items: list[OrderItem]):
    db.add_all(items)
    await db.flush()
    return items


async def delete_item(db: AsyncSession, item: OrderItem):
    await db.delete(item)


async def delete_items_by_order_id(db: AsyncSession, order_id: int):
    items = await get_items_by_order_id(db, order_id)
    for item in items:
        await db.delete(item)