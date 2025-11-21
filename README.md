# 記事サンプルリポジトリ

このリポジトリは、Python/TypeScript（バックエンド/フロントエンド）におけるテストの考え方と実践例を示すためのサンプルプロジェクトです。

## プロジェクト構成

```
test-article-sample-src/
├── backend/              # Django REST Framework バックエンド
│   ├── api/             # アプリケーションコード
│   │   ├── endpoints/   # エンドポイント別モジュール
│   │   ├── models/      # Djangoモデル
│   │   └── tests/       # テストコード
│   │       ├── unit/          # ユニットテスト
│   │       ├── integration/   # 統合テスト
│   │       ├── snapshot/      # スナップショットテスト
│   │       └── fixtures/      # テストヘルパー
│   └── config/          # Django設定
├── frontend/            # React + TypeScript フロントエンド
│   ├── src/            # ソースコード
│   └── tests/          # テストコード
│       ├── unit/            # ユニットテスト
│       └── integration/     # 統合テスト
└── docker-compose.yaml
```

## 技術スタック

### バックエンド
- **Python 3.11**
- **Django 5.2.8+**
- **Django REST Framework 3.16.1+**
- **pytest** - テストフレームワーク
- **pandas + pyarrow** - スナップショットテスト用
- **ruff** - Linter/Formatter
- **pyright** - 型チェック
- **uv** - パッケージマネージャー

### フロントエンド
- **React 18.3.1**
- **TypeScript 5.9.3**
- **Vite** - ビルドツール
- **Vitest** - テストフレームワーク
- **Testing Library** - コンポーネントテスト
- **Playwright** - E2Eテスト
- **Biome** - Linter/Formatter

## セットアップ

### 前提条件
- Python 3.11+
- Node.js 20+
- Docker & Docker Compose（オプション）

### ローカル環境でのセットアップ

#### バックエンド

```bash
cd backend

# uvをインストール（未インストールの場合）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 仮想環境を作成
uv venv

# 依存関係をインストール
uv pip install -e ".[dev]"

# マイグレーション実行
python manage.py migrate

# 開発サーバー起動
python manage.py runserver
```

#### フロントエンド

```bash
cd frontend

# 依存関係をインストール
npm install

# 開発サーバー起動
npm run dev
```

### Dockerでのセットアップ

```bash
# すべてのサービスを起動
docker-compose up

# バックエンド: http://localhost:8000
# フロントエンド: http://localhost:5173
```

## テストの実行

### バックエンドテスト

```bash
cd backend

# 全テスト実行
pytest

# ユニットテストのみ
pytest api/tests/unit/

# 統合テストのみ
pytest api/tests/integration/

# スナップショットテストのみ
pytest -m snapshot

# カバレッジ付きで実行
pytest --cov=api --cov-report=html

# Djangoテストランナーで実行
python manage.py test
```

### フロントエンドテスト

```bash
cd frontend

# 全テスト実行
npm test

# ウォッチモード
npm run test:watch

# カバレッジ付きで実行
npm run test:coverage

# UIモード
npm run test:ui
```

## Lint/Format

### バックエンド

```bash
cd backend

# Lintチェック
ruff check .

# 自動修正
ruff check --fix .

# フォーマット
ruff format .

# 型チェック
pyright
```

### フロントエンド

```bash
cd frontend

# Lintチェック
npm run lint

# 自動修正
npm run lint:fix

# フォーマット
npm run format
```

## テストの考え方

このリポジトリでは、以下の3種類のテスト例を提供しています：

### ✅ 良いテスト例（Good Examples）

- **目的が明確**: 何を検証しているかが明確
- **境界値テスト**: 0文字、200文字、201文字など
- **同値分割**: 有効な値、無効な値のパターン
- **スナップショットテスト**: ゴールデンデータとの比較
- **ハッピーパス**: 正常系の動作確認
- **異常系**: エラーハンドリングの確認

**例:**
```python
def test_title_boundary_max_length(self):
    max_title = "a" * 200
    todo = Todo.objects.create(title=max_title)
    assert len(todo.title) == 200

def test_title_boundary_exceeds_max_length(self):
    with pytest.raises(Exception):
        Todo.objects.create(title="a" * 201)
```

### ❌ 意味のないダメなテスト例（Bad Examples）

- **常にパス**: `assert True` など意味のないテスト
- **実装の詳細**: 内部実装に依存したテスト
- **フレームワークのテスト**: Djangoやフレームワーク自体の機能をテスト

**例:**
```python
def test_always_passes(self):
    assert True  # 意味がない

def test_implementation_detail(self):
    assert todo._state.db == "default"  # 実装詳細に依存
```

### 🔻 優先度の低いテスト例（Low Priority Examples）

- **getter/setterのみ**: 単純なアクセサのテスト
- **定数の確認**: 設定値の確認のみ
- **フレームワーク保証**: フレームワークが既に保証している動作

**例:**
```python
def test_str_method(self):
    todo = Todo.objects.create(title="Test TODO")
    assert str(todo) == "Test TODO"  # 優先度低

def test_meta_ordering(self):
    assert Todo._meta.ordering == ["-created_at"]  # 設定確認のみ
```

## スナップショットテスト

このプロジェクトでは、**ゴールデンデータを使用したスナップショットテスト**を採用しています。

### 仕組み

1. 期待される正しいAPIレスポンスをParquet形式で保存
2. テスト実行時に実際のレスポンスと比較
3. 差分があればテスト失敗

### メリット

- リグレッション検出に強い
- 大量のデータでも効率的に保存
- 実データとの完全一致を検証可能

**例:**
```python
def test_all_todos_snapshot(self, api_client):
    response = api_client.get("/api/todos/")
    data = response.json()

    snapshot_comparator.assert_matches_snapshot(
        data,
        "todos_all",
        exclude_fields=["id", "created_at", "updated_at"],
    )
```

## カバレッジ指標について

- **目標**: バックエンド 90%+、フロントエンド 80%+
- **注意点**:
  - 100%を目指す必要はない
  - getter/setterなどは除外してOK
  - 重要なビジネスロジックを優先
  - カバレッジは手段であり目的ではない

## API仕様

### エンドポイント

- `GET /api/todos/` - TODO一覧取得
  - クエリパラメータ: `completed`, `priority`, `overdue_only`
- `POST /api/todos/` - TODO作成
- `GET /api/todos/{id}/` - TODO詳細取得
- `PATCH /api/todos/{id}/` - TODO更新
- `DELETE /api/todos/{id}/` - TODO削除
- `POST /api/todos/{id}/toggle/` - 完了/未完了切り替え
- `DELETE /api/todos/bulk_delete_completed/` - 完了済み一括削除
- `GET /api/todos/statistics/` - 統計情報取得

### APIドキュメント

開発サーバー起動後、以下にアクセス:
- Swagger UI: http://localhost:8000/api/docs/
- OpenAPI Schema: http://localhost:8000/api/schema/

## Pre-commit Hooks

このプロジェクトでは、コミット前に自動でLint/Formatを実行します。

```bash
# バックエンド（リポジトリルートで）
pre-commit install

# コミット時に自動実行される
git commit -m "message"

# 手動実行
pre-commit run --all-files
```

## ライセンス

MIT License

## 参考資料

- [pytest公式ドキュメント](https://docs.pytest.org/)
- [Vitest公式ドキュメント](https://vitest.dev/)
- [Testing Library公式ドキュメント](https://testing-library.com/)
- [Django Testing](https://docs.djangoproject.com/en/stable/topics/testing/)
