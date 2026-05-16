from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.product import repository
from app.modules.product.model import Product


# -------------------------
# exceptions
# -------------------------

class ProductNotFound(Exception):
    pass


class InvalidProductData(Exception):
    pass


class InsufficientStock(Exception):
    pass


# -------------------------
# validation
# -------------------------

def _validate_price(price: int):
    if price < 0:
        raise InvalidProductData("Price cannot be negative")


def _validate_stock(stock: int):
    if stock < 0:
        raise InvalidProductData("Stock cannot be negative")


def _validate_quantity(qty: int):
    if qty <= 0:
        raise InvalidProductData("Quantity must be greater than 0")


# -------------------------
# create
# -------------------------

async def create_product(
    db: AsyncSession,
    name: str,
    description: str | None,
    price: int,
    stock: int,
    image_url: str | None,
) -> Product:

    _validate_price(price)
    _validate_stock(stock)

    product = Product(
        name=name,
        description=description,
        price=price,
        stock=stock,
        image_url=image_url,
        is_active=True,
    )

    await repository.create(db, product)
    await db.commit()
    await db.refresh(product)

    return product


# -------------------------
# read
# -------------------------

async def get_product_by_id(db: AsyncSession, product_id: int) -> Product:
    product = await repository.get_by_id(db, product_id)

    if not product:
        raise ProductNotFound()

    return product


async def get_all_active_products(db: AsyncSession) -> list[Product]:
    return await repository.get_all_active(db)


# -------------------------
# update
# -------------------------

async def update_product(
    db: AsyncSession,
    product: Product,
    name: str,
    description: str | None,
    price: int,
    stock: int,
    image_url: str | None,
    is_active: bool,
) -> Product:

    _validate_price(price)
    _validate_stock(stock)

    product.name = name
    product.description = description
    product.price = price
    product.stock = stock
    product.image_url = image_url
    product.is_active = is_active

    await repository.save(db, product)
    await db.commit()
    await db.refresh(product)

    return product


# -------------------------
# delete (soft)
# -------------------------

async def delete_product(db: AsyncSession, product: Product) -> Product:

    product.is_active = False

    await repository.soft_delete(db, product)
    await db.commit()
    await db.refresh(product)

    return product


# -------------------------
# stock
# -------------------------

async def decrease_stock(
    db: AsyncSession,
    product_id: int,
    quantity: int,
) -> None:

    _validate_quantity(quantity)

    ok = await repository.decrease_stock(db, product_id, quantity)

    if not ok:
        raise InsufficientStock()

    await db.commit()