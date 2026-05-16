EC App

FastAPI + React + PostgreSQL を用いた EC サービスです。

JWT 認証、権限制御、注文トランザクション、状態遷移制御を実装し、
業務システムを意識したバックエンド設計を行いました。

Docker による開発環境統一、Alembic によるマイグレーション管理にも対応しています。

Demo
Demo Video

動画リンク

Features
Authentication
JWT Authentication
Access Token / Refresh Token 分離
Password Hashing（Argon2）
権限制御（Admin / User）
Product
商品一覧・詳細取得
商品作成（Admin）
在庫管理
論理削除
Cart
カート追加・削除
カート一覧取得
Order
注文作成
注文履歴・詳細取得
注文ステータス更新
状態遷移制御
Business Logic
Transaction Management

注文作成時は、

在庫確認
注文生成
在庫更新

を単一トランザクションとして管理し、データ整合性を維持しています。

try:
    ...
    await db.commit()

except Exception:
    await db.rollback()

在庫不足時は注文を中断します。

if product.stock < item["quantity"]:
    raise ValueError("insufficient stock")
Order Status Transition

注文ステータスの不正更新を防ぐため、
遷移可能状態を制御しています。

allowed_transitions = {
    OrderStatus.PENDING: [
        OrderStatus.PAID,
        OrderStatus.CANCELLED,
    ],
    OrderStatus.PAID: [
        OrderStatus.SHIPPED
    ],
}
Architecture

レイヤードアーキテクチャを採用しています。

router      # API endpoint
service     # business logic
repository  # DB access
model       # ORM model
schema      # Pydantic schema
Design
Service 層へ業務ロジックを集約
Repository 層で DB アクセスを抽象化
Transaction 境界を Service 層で管理
状態遷移ルールを集約し、不正更新を防止

FastAPI の Depends を利用し、認証・認可を実装しています。

API
POST /auth/login
POST /orders/
GET  /orders/me
PUT  /orders/{id}/status
POST /cart/
Tech Stack
Backend
FastAPI
SQLAlchemy（Async）
PostgreSQL
Alembic
python-jose（JWT）
Passlib / Argon2
Pytest
Frontend
React（Vite）
React Router
Axios
Infrastructure
Docker
Docker Compose
Testing

pytest + httpx を用いて API テストを実装しています。

Test Cases
ログイン認証
注文作成
在庫不足
注文詳細取得
ステータス更新
不正状態遷移

主要業務ロジックを中心に、正常系・異常系の両方をテストしています。

Development
Start
docker compose up --build
Migration
alembic upgrade head
Test
pytest --cov
Future Improvements
Refresh Token Rotation
Redis Cache
CI/CD
Stripe 決済対応
AWS Deploy
RBAC 拡張
Motivation

単なる CRUD 実装ではなく、

認証
権限制御
トランザクション
状態遷移
保守性

を意識し、業務システムを想定した設計・実装を行いました。