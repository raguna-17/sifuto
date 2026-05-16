from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.order import repository
from app.modules.product.repository import get_by_id
from app.modules.order.model import Order, OrderItem
from app.core.enums import OrderStatus


# =========================================================
# 注文作成（トランザクション安全版）
# =========================================================

async def create_order(
    db: AsyncSession,
    user_id: int,
    items: list[dict],  # [{"product_id": 1, "quantity": 2}]
):
    try:
        if not items:
            return None

        # -------------------------
        # 事前検証（読み取りフェーズ）
        # -------------------------
        products_to_use = []
        total_price = 0

        for item in items:
            product = await get_by_id(db, item["product_id"])

            if not product:
                raise ValueError("product not found")

            if product.stock < item["quantity"]:
                raise ValueError("insufficient stock")

            products_to_use.append((product, item["quantity"]))
            total_price += product.price * item["quantity"]

        # -------------------------
        # Order作成（まだ副作用なし）
        # -------------------------
        order = Order(
            user_id=user_id,
            status=OrderStatus.PENDING,
            total_price=total_price,
        )

        await repository.add_order(db, order)

        # -------------------------
        # OrderItem作成（関連付けのみ）
        # -------------------------
        order_items = []

        for product, qty in products_to_use:
            order_items.append(
                OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    quantity=qty,
                    price_at_purchase=product.price,
                )
            )

        await repository.add_items(db, order_items)

        # -------------------------
        # 副作用フェーズ（ここで初めて状態変更）
        # -------------------------
        for product, qty in products_to_use:
            product.stock -= qty

        # -------------------------
        # commit（唯一の確定ポイント）
        # -------------------------
        await db.commit()
        await db.refresh(order)

        return order

    except Exception:
        await db.rollback()
        raise


# =========================================================
# ユーザー注文一覧
# =========================================================

async def get_user_orders(db: AsyncSession, user_id: int):
    return await repository.get_orders_by_user(db, user_id)


# =========================================================
# 注文詳細（所有者チェック）
# =========================================================

async def get_order_detail(
    db: AsyncSession,
    order_id: int,
    user_id: int,
):
    order = await repository.get_order_by_id(db, order_id)

    if not order:
        return None

    if order.user_id != user_id:
        return None

    return order


# =========================================================
# ステータス更新（安全なトランザクション）
# =========================================================

async def update_order_status(
    db: AsyncSession,
    order_id: int,
    status: OrderStatus,
):
    try:
        order = await repository.get_order_by_id(db, order_id)

        if not order:
            return None

        allowed_transitions = {
            OrderStatus.PENDING: [OrderStatus.PAID, OrderStatus.CANCELLED],
            OrderStatus.PAID: [OrderStatus.SHIPPED],
            OrderStatus.SHIPPED: [],
            OrderStatus.CANCELLED: [],
        }

        if status not in allowed_transitions.get(order.status, []):
            return None

        order.status = status

        await db.commit()
        await db.refresh(order)

        return order

    except Exception:
        await db.rollback()
        raise


# =========================================================
# 削除（安全版）
# =========================================================

async def delete_order(db: AsyncSession, order_id: int):
    try:
        order = await repository.get_order_by_id(db, order_id)

        if not order:
            return False

        await repository.delete_items_by_order_id(db, order.id)
        await repository.delete_order(db, order)

        await db.commit()
        return True

    except Exception:
        await db.rollback()
        raise


# =========================================================
# 管理用
# =========================================================

async def get_all_orders(db: AsyncSession):
    return await repository.get_all_orders(db)