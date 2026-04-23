📄 Job Application Management API

企業への応募状況を一元管理できるWebアプリのバックエンドAPIです。
実際の転職・就職活動における情報管理を想定し、応募・企業・ユーザー情報を統合的に扱えるよう設計しています。

実務を意識し、以下を重視しています：

セキュアな認証設計（JWT）
フロントエンドとバックエンドの疎結合構成
ドメイン単位での責務分離
保守性・拡張性を考慮したアーキテクチャ設計
🚀 技術スタック
バックエンド
Python 3.12
FastAPI
SQLAlchemy（Async ORM）
PostgreSQL（想定）
Alembic（マイグレーション管理）
JWT認証（python-jose）
Argon2（パスワードハッシュ）
Docker / Docker Compose
🧱 アーキテクチャ設計

ドメイン駆動を意識したレイヤード構成を採用しています。

各ドメインは以下の責務に分離：

router：APIエンドポイント定義
service：ビジネスロジック
model：DBモデル定義
schema：入出力スキーマ
app/
├── users
├── organizations
├── job_applications
├── core
└── db / dependencies
🔐 認証設計

JWTベースの認証を採用し、ステートレスなAPI設計を実現しています。

認証フロー
ログイン時にJWTトークンを発行
トークンからユーザーIDを取得
DBと照合し認証を検証
セキュリティ
パスワードはArgon2でハッシュ化
トークンベース認証によるスケーラビリティ確保
👤 ユーザー機能

ユーザー単位で認証・データ管理を行います。

エンドポイント
Method	Path	Description
POST	/users/register	ユーザー登録
POST	/users/login	ログイン
GET	/users/me	認証ユーザー取得
🏢 企業管理（Organizations）

ユーザーごとに企業情報を管理できます。

エンドポイント
Method	Path	Description
POST	/organizations	企業作成
GET	/organizations	一覧取得
GET	/organizations/{id}	詳細取得
DELETE	/organizations/{id}	削除
💼 応募管理（Job Applications）

企業への応募履歴を管理します。

エンドポイント
Method	Path	Description
POST	/job-applications	応募作成
GET	/job-applications	自分の応募一覧
GET	/job-applications/{id}	応募詳細
DELETE	/job-applications/{id}	削除
🗄 データモデル設計
User
email
hashed_password
is_active
created_at

リレーション：

organizations
job_applications
Organization
name
industry
user_id

リレーション：

job_applications
JobApplication
user_id
organization_id
organization_name
job_title
created_at
📌 設計上の特徴
ドメイン単位での責務分離（レイヤードアーキテクチャ）
非同期処理（AsyncSession）によるパフォーマンス最適化
JWT認証によるステートレス設計
ユーザー単位でのデータ分離
REST API設計の採用
Service層によるビジネスロジック分離
ユニーク制約によるデータ整合性の担保
📂 フロントエンド連携

React（Vite）によるSPA構成

auth
organizations
job_applications

各機能ごとにAPI層を分離し、責務を明確化しています。

🧪 テスト

pytestを用いてAPIテストを実装しています。

ユーザー登録
ログイン
認証フロー

正常系・異常系の両方をカバーし、リファクタリングや機能追加に耐えられる構成としています。

📈 今後の改善・拡張
ページネーションの導入
検索機能の追加
ロール管理（admin / user）
Redisキャッシュ導入
CI/CD構築
エラーハンドリングの標準化
UI/UX改善
🧑‍💻 ポートフォリオ情報

個人開発プロジェクト（求人管理システム）