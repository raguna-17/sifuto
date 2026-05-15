from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.core.security import get_current_user, require_role

from app.modules.order import service
from app.modules.order.schema import (
    OrderCreate,
    OrderResponse,
    OrderUpdate,
)

router = APIRouter(prefix="/orders", tags=["orders"])


# =========================================================
# 👤 ユーザー：注文作成
# =========================================================

@router.post("/", response_model=OrderResponse)
async def create_order(
    payload: OrderCreate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    order = await service.create_order(
        db=db,
        user_id=user.id,
        items=[item.model_dump() for item in payload.items],
    )

    if not order:
        raise HTTPException(status_code=400, detail="Order creation failed")

    return order


# =========================================================
# 👤 ユーザー：自分の注文一覧
# =========================================================

@router.get("/", response_model=list[OrderResponse])
async def get_my_orders(
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    return await service.get_user_orders(db, user.id)


# =========================================================
# 👤 ユーザー：注文詳細
# =========================================================

@router.get("/{order_id}", response_model=OrderResponse)
async def get_order_detail(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    order = await service.get_order_detail(
        db=db,
        order_id=order_id,
        user_id=user.id,
    )

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return order


# =========================================================
# 👤 ユーザー：キャンセル
# =========================================================

@router.delete("/{order_id}")
async def cancel_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    success = await service.cancel_order(
        db=db,
        order_id=order_id,
        user_id=user.id,
    )

    if not success:
        raise HTTPException(status_code=400, detail="Cannot cancel order")

    return {"message": "canceled"}


# =========================================================
# 🛠 ADMIN
# =========================================================

@router.get("/admin/all", response_model=list[OrderResponse])
async def get_all_orders(
    db: AsyncSession = Depends(get_db),
    admin=Depends(require_role("admin")),
):
    return await service.get_all_orders(db)


# -------------------------
# ステータス更新
# -------------------------

@router.patch("/admin/{order_id}/status", response_model=OrderResponse)
async def update_order_status(
    order_id: int,
    payload: OrderUpdate,
    db: AsyncSession = Depends(get_db),
    admin=Depends(require_role("admin")),
):
    order = await service.update_order_status(
        db=db,
        order_id=order_id,
        status=payload.status,
    )

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return order


# -------------------------
# 削除
# -------------------------

@router.delete("/admin/{order_id}")
async def delete_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    admin=Depends(require_role("admin")),
):
    success = await service.delete_order(db, order_id)

    if not success:
        raise HTTPException(status_code=404, detail="Order not found")

    return {"message": "deleted"}