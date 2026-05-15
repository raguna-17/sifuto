from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.order import repository
from app.modules.product.repository import get_product_by_id
from app.modules.order.model import Order, OrderItem
from app.core.enums import OrderStatus


# =========================================================
# 注文作成（コアビジネスロジック）
# =========================================================

async def create_order(
    db: AsyncSession,
    user_id: int,
    items: list[dict],  # [{"product_id": 1, "quantity": 2}]
):
    if not items:
        return None

    order_items: list[OrderItem] = []
    total_price = 0

    # -------------------------
    # 商品チェック & 金額計算
    # -------------------------
    for item in items:
        product = await get_product_by_id(db, item["product_id"])

        if not product:
            return None

        if product.stock < item["quantity"]:
            return None

        price = product.price * item["quantity"]
        total_price += price

        order_items.append(
            OrderItem(
                product_id=product.id,
                quantity=item["quantity"],
                price_at_purchase=product.price,
            )
        )

        # 在庫減少
        product.stock -= item["quantity"]

    # -------------------------
    # Order作成（ヘッダー）
    # -------------------------
    order = Order(
        user_id=user_id,
        status=OrderStatus.PENDING,
        total_price=total_price,
    )

    await repository.add_order(db, order)

    # -------------------------
    # OrderItem作成（明細）
    # -------------------------
    for item in order_items:
        item.order_id = order.id

    await repository.add_items(db, order_items)

    await db.commit()
    await db.refresh(order)

    return order


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
# ステータス更新（管理 or 制御ロジック）
# =========================================================

async def update_order_status(
    db: AsyncSession,
    order_id: int,
    status: OrderStatus,
):
    order = await repository.get_order_by_id(db, order_id)

    if not order:
        return None

    # 状態遷移ルール（必要ならここに追加）
    allowed_transitions = {
        OrderStatus.PENDING: [OrderStatus.PAID, OrderStatus.CANCELLED],
        OrderStatus.PAID: [OrderStatus.SHIPPED],
        OrderStatus.SHIPPED: [],
        OrderStatus.CANCELLED: [],
    }

    if status not in allowed_transitions.get(order.status, []):
        return None

    return await repository.update_order_status(db, order, status)


# =========================================================
# 削除（管理用）
# =========================================================

async def delete_order(db: AsyncSession, order_id: int):
    order = await repository.get_order_by_id(db, order_id)

    if not order:
        return False

    # 明細も削除
    await repository.delete_items_by_order_id(db, order.id)
    await repository.delete_order(db, order)

    await db.commit()
    return True


# =========================================================
# 管理用：全注文
# =========================================================

async def get_all_orders(db: AsyncSession):
    return await repository.get_all_orders(db)