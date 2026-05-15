from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.product import repository
from app.modules.product.model import Product


# -------------------------
# Exceptions
# -------------------------

class ProductNotFound(Exception):
    pass


class InvalidProductData(Exception):
    pass


class InsufficientStock(Exception):
    pass


# -------------------------
# validators
# -------------------------

def _validate_price(price: int):
    if price < 0:
        raise InvalidProductData("Price cannot be negative")


def _validate_stock(stock: int):
    if stock < 0:
        raise InvalidProductData("Stock cannot be negative")


def _validate_quantity(quantity: int):
    if quantity <= 0:
        raise InvalidProductData("Quantity must be greater than 0")


# -------------------------
# create product
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

    return await repository.create(db, product)


# -------------------------
# get product
# -------------------------

async def get_product_by_id(
    db: AsyncSession,
    product_id: int,
) -> Product:

    product = await repository.get_product_by_id(db, product_id)

    if product is None:
        raise ProductNotFound(f"Product {product_id} not found")

    return product


# -------------------------
# list active products
# -------------------------

async def get_all_active_products(db: AsyncSession) -> list[Product]:
    return await repository.get_all_active_products(db)


# -------------------------
# update product
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

    return await repository.save(db, product)


# -------------------------
# soft delete
# -------------------------

async def delete_product(
    db: AsyncSession,
    product: Product,
) -> Product:

    return await repository.soft_delete(db, product)


# -------------------------
# decrease stock
# -------------------------

async def decrease_stock(
    db: AsyncSession,
    product: Product,
    quantity: int,
) -> Product:

    _validate_quantity(quantity)

    if product.stock < quantity:
        raise InsufficientStock("Not enough stock")

    product.stock -= quantity

    return await repository.save(db, product)