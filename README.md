家計簿管理アプリ（Full Stack）
■ 概要

本アプリケーションは、支出・収入・カテゴリを分離設計したフルスタック家計簿管理システムです。
React + FastAPI によるAPI分離構成を採用し、JWT認証・ドメイン駆動的なレイヤー分割（router / service / repository）で実装しています。

■ 技術スタック
Frontend
React
Vite
React Router
Axios
Backend
FastAPI
SQLAlchemy
Alembic
Pydantic
JWT認証（OAuth2 Password Flow）
Database
PostgreSQL
Infrastructure
Docker / Docker Compose
Testing
pytest
■ アーキテクチャ設計
フロントエンド設計
featureベースディレクトリ構成
API層とUI層の分離
再利用可能な共通コンポーネント設計（Button / Input / Modal）
バックエンド設計
ドメイン単位でモジュール分割（users / finance）
router / service / repository の責務分離
ビジネスロジックをservice層に集約
DBアクセスをrepository層に分離
設計思想
関心の分離（Separation of Concerns）
スケーラビリティを意識した構造設計
フロント・バックエンド完全分離構成
■ 主な機能
認証
ユーザー登録
JWTログイン認証
ユーザー状態管理
支出管理
支出CRUD
カテゴリ紐付け
一覧取得
収入管理
収入CRUD
一覧取得
カテゴリ管理
カテゴリCRUD
■ API設計

RESTful APIを採用し、リソース単位で設計。

Auth
POST /auth/register
POST /auth/login
Expenses
GET /expenses
POST /expenses
PUT /expenses/{id}
DELETE /expenses/{id}
Incomes
GET /incomes
POST /incomes
PUT /incomes/{id}
DELETE /incomes/{id}
Categories
GET /categories
POST /categories
■ セットアップ
Backend
pip install -r requirements.txt
uvicorn app.main:app --reload
Frontend
npm install
npm run dev
Docker
docker-compose up --build
■ 環境変数
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
SECRET_KEY=your_secret_key
ALGORITHM=HS256
■ 工夫した点（ここ重要）
ビジネスロジックをservice層へ分離
DBアクセスをrepository層で統一管理
feature単位でフロントを分割し保守性を向上
JWT認証によるセキュアなAPI設計
フロントとバックの完全分離構成
■ 改善予定
月次収支グラフの可視化
カテゴリ別支出分析
集計ダッシュボード追加
本番環境デプロイ（Render / Railway / AWS）
■ 採用観点でのポイント
API設計とレイヤー分割の理解
フルスタック構成の実装経験
認証機構の実装経験
Dockerによる開発環境構築
スケーラブルなディレクトリ設計