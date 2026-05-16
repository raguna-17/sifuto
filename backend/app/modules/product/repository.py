from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.product.model import Product


async def get_by_id(db: AsyncSession, product_id: int) -> Product | None:
    result = await db.execute(
        select(Product).where(Product.id == product_id)
    )
    return result.scalar_one_or_none()


async def get_all(db: AsyncSession) -> list[Product]:
    result = await db.execute(select(Product))
    return result.scalars().all()


async def get_all_active(db: AsyncSession) -> list[Product]:
    result = await db.execute(
        select(Product).where(Product.is_active.is_(True))
    )
    return result.scalars().all()


async def create(db: AsyncSession, product: Product) -> Product:
    db.add(product)
    return product


async def save(db: AsyncSession, product: Product) -> Product:
    db.add(product)
    return product


async def decrease_stock(db: AsyncSession, product_id: int, quantity: int) -> bool:
    stmt = (
        update(Product)
        .where(Product.id == product_id)
        .where(Product.stock >= quantity)
        .values(stock=Product.stock - quantity)
    )

    result = await db.execute(stmt)
    return result.rowcount > 0


async def soft_delete(db: AsyncSession, product: Product) -> Product:
    product.is_active = False
    return product