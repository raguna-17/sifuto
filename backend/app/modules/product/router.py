from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.modules.product import service, schema

from app.core.enums import UserRole
from app.core.security import require_role

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


# -------------------------
# exception mapping
# -------------------------

def handle_error(e: Exception):
    if isinstance(e, service.ProductNotFound):
        raise HTTPException(status_code=404, detail="Product not found")

    if isinstance(e, service.InvalidProductData):
        raise HTTPException(status_code=400, detail=str(e))

    if isinstance(e, service.InsufficientStock):
        raise HTTPException(status_code=409, detail="Insufficient stock")

    raise HTTPException(status_code=500, detail="Unexpected error")


# -------------------------
# create (admin)
# -------------------------

@router.post("/", response_model=schema.ProductRead)
async def create_product(
    payload: schema.ProductCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_role(UserRole.ADMIN)),
):
    try:
        return await service.create_product(
            db,
            payload.name,
            payload.description,
            payload.price,
            payload.stock,
            payload.image_url,
        )
    except Exception as e:
        handle_error(e)


# -------------------------
# list
# -------------------------

@router.get("/", response_model=list[schema.ProductRead])
async def get_products(db: AsyncSession = Depends(get_db)):
    return await service.get_all_active_products(db)


# -------------------------
# get by id
# -------------------------

@router.get("/{product_id}", response_model=schema.ProductRead)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await service.get_product_by_id(db, product_id)
    except Exception as e:
        handle_error(e)


# -------------------------
# update (admin)
# -------------------------

@router.put("/{product_id}", response_model=schema.ProductRead)
async def update_product(
    product_id: int,
    payload: schema.ProductUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_role(UserRole.ADMIN)),
):
    try:
        product = await service.get_product_by_id(db, product_id)

        return await service.update_product(
            db,
            product,
            payload.name,
            payload.description,
            payload.price,
            payload.stock,
            payload.image_url,
            payload.is_active,
        )

    except Exception as e:
        handle_error(e)


# -------------------------
# delete (soft)
# -------------------------

@router.delete("/{product_id}")
async def delete_product(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_role(UserRole.ADMIN)),
):
    try:
        product = await service.get_product_by_id(db, product_id)
        await service.delete_product(db, product)
        return {"message": "deleted"}

    except Exception as e:
        handle_error(e)