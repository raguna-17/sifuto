from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.modules.product.model import Product


# -------------------------
# Read
# -------------------------

async def get_product_by_id(db: AsyncSession, product_id: int) -> Product | None:
    result = await db.execute(
        select(Product).where(Product.id == product_id)
    )
    return result.scalar_one_or_none()


async def get_all_products(db: AsyncSession) -> list[Product]:
    result = await db.execute(
        select(Product)
    )
    return result.scalars().all()


async def get_all_active_products(db: AsyncSession) -> list[Product]:
    result = await db.execute(
        select(Product).where(Product.is_active.is_(True))
    )
    return result.scalars().all()


# -------------------------
# Create
# -------------------------

async def create(db: AsyncSession, product: Product) -> Product:
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product


# -------------------------
# Save (update共通)
# -------------------------

async def save(db: AsyncSession, product: Product) -> Product:
    db.add(product)  # 既存でもOK（merge的扱い）
    await db.commit()
    await db.refresh(product)
    return product


# -------------------------
# Soft Delete
# -------------------------

async def soft_delete(db: AsyncSession, product: Product) -> Product:
    product.is_active = False
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product