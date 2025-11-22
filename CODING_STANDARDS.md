# コーディング規約

> このドキュメントは、プロジェクトに参加する全ての開発者が遵守すべきコーディング規約を定めます。
> 本規約に従うことで、コードの一貫性、可読性、保守性を保ちます。

**最終更新日**: 2025-11-22

---

## 目次

1. [プロジェクト概要](#プロジェクト概要)
2. [開発環境セットアップ](#開発環境セットアップ)
3. [ディレクトリ構造規約](#ディレクトリ構造規約)
4. [コーディングスタイル規約](#コーディングスタイル規約)
5. [命名規則](#命名規則)
6. [ドキュメンテーション規約](#ドキュメンテーション規約)
7. [テスト規約](#テスト規約)
8. [リンター・フォーマッタ設定](#リンターフォーマッタ設定)
9. [pre-commit設定](#pre-commit設定)
10. [Git規約](#git規約)
11. [IDE設定（VSCode）](#ide設定vscode)
12. [CI/CD規約](#cicd規約)
13. [依存関係管理規約](#依存関係管理規約)

---

## プロジェクト概要

### 技術スタック

**バックエンド**:
- Python 3.11+
- Django 5.2+
- Django REST Framework 3.16+
- pytest 8.0+（テストフレームワーク）
- Ruff 0.14+（リンター・フォーマッタ）
- uv（パッケージマネージャー）

**フロントエンド**:
- TypeScript 5.9+
- React 18.3+
- Vite 7.1+（ビルドツール）
- Vitest 4.0+（テストフレームワーク）
- Biome 2.2+（リンター・フォーマッタ）
- npm（パッケージマネージャー）

### プロジェクト構成

```
.
├── backend/               # Django REST API
├── frontend/              # React + Vite SPA
├── .vscode/               # VSCode設定
├── .pre-commit-config.yaml
├── docker-compose.yaml
└── README.md
```

---

## 開発環境セットアップ

### 必須ツール

1. **Python 3.11以上**
2. **Node.js 20以上**
3. **uv** (Python パッケージマネージャー)
4. **Git**
5. **VSCode** (推奨エディタ)

### セットアップ手順

#### 1. バックエンド環境構築

```bash
cd backend

# 仮想環境作成
uv venv

# 依存関係インストール（開発用を含む）
uv pip install -e ".[dev]"

# マイグレーション実行
python manage.py migrate

# 開発サーバー起動
python manage.py runserver
```

#### 2. フロントエンド環境構築

```bash
cd frontend

# 依存関係インストール
npm install

# 開発サーバー起動
npm run dev
```

#### 3. pre-commit設定

```bash
# ルートディレクトリで実行
pre-commit install

# 手動実行
pre-commit run --all-files
```

#### 4. Docker環境（オプション）

```bash
# ルートディレクトリで実行
docker-compose up
```

---

## ディレクトリ構造規約

### バックエンド構造

```
backend/
├── .python-version         # Python 3.11指定
├── .pre-commit-config.yaml # バックエンド専用pre-commit設定
├── pyproject.toml          # 依存関係・ツール設定
├── uv.lock                 # ロックファイル
├── manage.py               # Django管理コマンド
├── config/                 # プロジェクト設定
│   ├── __init__.py
│   ├── settings.py         # Django設定
│   ├── urls.py             # ルートURL設定
│   ├── asgi.py
│   ├── wsgi.py
│   └── test_runner.py      # カスタムテストランナー
└── api/                    # メインアプリケーション
    ├── __init__.py
    ├── admin.py            # Django Admin設定
    ├── apps.py
    ├── urls.py             # APIルーティング
    ├── models/             # モデル層（データ構造）
    │   ├── __init__.py
    │   └── todo.py
    ├── endpoints/          # エンドポイント層（ビジネスロジック）
    │   ├── __init__.py
    │   └── todos/
    │       ├── __init__.py
    │       ├── views.py        # ViewSet（エンドポイント定義）
    │       ├── serializers.py  # シリアライザー（データ変換）
    │       └── services.py     # サービス層（ビジネスロジック）
    ├── migrations/         # データベースマイグレーション
    │   └── __init__.py
    └── tests/              # テストコード
        ├── __init__.py
        ├── conftest.py     # pytestフィクスチャ（共通設定）
        ├── unit/           # ユニットテスト
        │   ├── __init__.py
        │   ├── test_models.py
        │   ├── test_serializers.py
        │   └── test_services.py
        ├── integration/    # 統合テスト
        │   ├── __init__.py
        │   └── test_api.py
        ├── snapshot/       # スナップショットテスト
        │   ├── __init__.py
        │   ├── test_todos.py
        │   └── README.md
        └── fixtures/       # テストヘルパー
            ├── __init__.py
            └── snapshot_helpers.py
```

**重要な構造規則**:

1. **レイヤー分離**: モデル → シリアライザー → サービス → ビューセットの順に依存
2. **エンドポイント単位でディレクトリ分割**: `endpoints/todos/` のように機能ごとにディレクトリを作成
3. **テストは3層構造**: `unit/`, `integration/`, `snapshot/` で明確に分離
4. **フィクスチャは共通化**: `conftest.py` にグローバルフィクスチャを配置

### フロントエンド構造

```
frontend/
├── .gitignore
├── .husky/                 # Git hooks（pre-commit）
│   └── pre-commit
├── index.html              # HTMLエントリーポイント
├── package.json            # npm依存関係
├── package-lock.json
├── tsconfig.json           # TypeScript設定
├── tsconfig.node.json      # ツール用TypeScript設定
├── vite.config.ts          # Vite設定
├── vitest.config.ts        # Vitest設定
├── biome.json              # Biome設定
├── src/
│   ├── main.tsx            # アプリケーションエントリーポイント
│   ├── App.tsx             # ルートコンポーネント
│   ├── index.css           # グローバルスタイル
│   ├── vite-env.d.ts       # Vite型定義
│   ├── components/         # Reactコンポーネント
│   │   ├── TodoForm.tsx
│   │   ├── TodoList.tsx
│   │   └── TodoItem.tsx
│   ├── services/           # API通信サービス
│   │   └── TodoService.ts
│   └── types/              # TypeScript型定義
│       └── index.ts
└── tests/
    ├── setup/
    │   └── setupTests.ts   # テストセットアップ
    └── unit/
        ├── components/     # コンポーネントテスト
        │   ├── TodoForm.test.tsx
        │   ├── TodoList.test.tsx
        │   └── TodoItem.test.tsx
        └── services/       # サービステスト
            └── TodoService.test.ts
```

**重要な構造規則**:

1. **機能ベース分割**: `components/`, `services/`, `types/` のように機能ごとにディレクトリ分割
2. **テストはソースと分離**: `tests/` ディレクトリに集約（ソースコードと同じディレクトリ構造を維持）
3. **型定義の集約**: `types/index.ts` に全ての型定義を配置
4. **Path Alias使用**: `@/` でsrcディレクトリを参照（例: `import { Todo } from "@/types"`）

---

## コーディングスタイル規約

### Python（バックエンド）

#### 基本スタイル

- **行の長さ**: 最大88文字（Black/Ruff標準）
- **インデント**: スペース4つ
- **文字列**: ダブルクォート `"` を優先
- **インポート順序**: 標準ライブラリ → サードパーティ → ローカル

#### インポート順序

```python
# 1. 標準ライブラリ
from datetime import date, timedelta
from pathlib import Path

# 2. サードパーティ
from django.db import models
from rest_framework import serializers

# 3. ローカルアプリケーション
from api.models.todo import Todo
from config.settings import BASE_DIR
```

Ruffの`isort`が自動で整形します。

#### 型アノテーション

**必須箇所**:
- 全ての関数のパラメータと戻り値
- パブリックメソッド
- 複雑な変数

**例**:
```python
def get_todos(
    completed: bool | None = None,
    priority: str | None = None,
) -> QuerySet[Todo]:
    """TODOのクエリセットを取得する。

    Args:
        completed: 完了状態でフィルタ（None=全て）
        priority: 優先度でフィルタ（None=全て）

    Returns:
        QuerySet[Todo]: フィルタ済みTODOクエリセット
    """
    queryset = Todo.objects.all()

    if completed is not None:
        queryset = queryset.filter(completed=completed)

    if priority:
        queryset = queryset.filter(priority=priority)

    return queryset
```

#### Djangoモデルの規約

```python
class Todo(models.Model):
    """TODOアイテムを表すモデル。

    Attributes:
        title (str): TODOのタイトル
        completed (bool): 完了状態
    """

    # 定数は大文字
    PRIORITY_LOW = "low"
    PRIORITY_MEDIUM = "medium"
    PRIORITY_HIGH = "high"

    PRIORITY_CHOICES = [
        (PRIORITY_LOW, "Low"),
        (PRIORITY_MEDIUM, "Medium"),
        (PRIORITY_HIGH, "High"),
    ]

    # フィールド定義
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default=PRIORITY_MEDIUM,
    )

    class Meta:
        db_table = "todos"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["completed"]),
            models.Index(fields=["priority"]),
        ]

    def __str__(self):
        return self.title
```

**重要なポイント**:
1. モデル定数は大文字スネークケース
2. `Meta` クラスで `db_table`, `ordering`, `indexes` を明示
3. `__str__` メソッドを必ず実装

### TypeScript/React（フロントエンド）

#### 基本スタイル

- **行の長さ**: 最大100文字
- **インデント**: スペース2つ
- **文字列**: ダブルクォート `"` を使用
- **セミコロン**: 必須
- **クォートスタイル**: `quoteStyle: "double"`

#### インポート順序

```typescript
// 1. React imports
import type { FC, ReactNode } from "react";
import { useState, useEffect } from "react";

// 2. 外部パッケージ
import { format } from "date-fns";

// 3. ローカルインポート（型定義優先）
import type { Todo, TodoCreate } from "@/types";
import TodoService from "@/services/TodoService";
import TodoItem from "@/components/TodoItem";
```

Biomeが自動で整形します。

#### 型定義

**型 vs インターフェース**:
- **Utility Types**: `type` を使用（例: `type Priority = "low" | "medium" | "high"`）
- **オブジェクト構造**: `interface` を使用（例: `interface Todo { ... }`）

```typescript
// Utility Types
export type Priority = "low" | "medium" | "high";

// インターフェース
export interface Todo {
  id: number;
  title: string;
  completed: boolean;
  priority: Priority;
  due_date: string | null;
}

export interface TodoCreate {
  title: string;
  description?: string;
  priority?: Priority;
  due_date?: string | null;
}
```

#### Reactコンポーネント

```typescript
/**
 * @fileoverview TODO作成フォームコンポーネント
 */

import type { Priority, TodoCreate } from "@/types";
import { useState } from "react";

/**
 * TODOフォームのプロパティ
 */
interface TodoFormProps {
  /** フォーム送信時のコールバック関数 */
  onSubmit: (todo: TodoCreate) => void;
  /** キャンセルボタン押下時のコールバック関数（オプション） */
  onCancel?: () => void;
}

/**
 * TODO作成フォームコンポーネント
 *
 * 新しいTODOを作成するためのフォームを表示します。
 *
 * @param {TodoFormProps} props - コンポーネントのプロパティ
 * @returns {JSX.Element} TODOフォーム
 */
export default function TodoForm({ onSubmit, onCancel }: TodoFormProps) {
  const [title, setTitle] = useState("");
  const [priority, setPriority] = useState<Priority>("medium");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!title.trim()) {
      alert("タイトルを入力してください");
      return;
    }

    onSubmit({
      title: title.trim(),
      priority,
    });

    // フォームリセット
    setTitle("");
    setPriority("medium");
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label htmlFor="title">タイトル *</label>
        <input
          type="text"
          id="title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          maxLength={200}
          required
        />
      </div>

      <button type="submit">作成</button>
    </form>
  );
}
```

**重要なポイント**:
1. `@fileoverview` でファイル説明を記載
2. Propsは `interface` で定義
3. JSDocコメントでコンポーネント説明
4. デフォルトエクスポートを使用
5. イベントハンドラは `handle` プレフィックス

---

## 命名規則

### Python

| 種類 | 規則 | 例 |
|------|------|-----|
| クラス名 | PascalCase | `Todo`, `TodoViewSet` |
| 関数・メソッド | snake_case | `get_todos`, `is_overdue` |
| 変数 | snake_case | `todo_list`, `created_at` |
| 定数 | UPPER_CASE | `PRIORITY_HIGH`, `MAX_LENGTH` |
| プライベートメソッド | _leading_underscore | `_internal_method` |
| モジュール名 | snake_case | `todo.py`, `snapshot_helpers.py` |

### TypeScript/React

| 種類 | 規則 | 例 |
|------|------|-----|
| コンポーネント名 | PascalCase | `TodoForm`, `TodoItem` |
| インターフェース | PascalCase | `TodoFormProps`, `Todo` |
| 関数・変数 | camelCase | `handleSubmit`, `todoList` |
| 定数 | camelCase or UPPER_CASE | `API_BASE_URL`, `maxLength` |
| ファイル名（コンポーネント） | PascalCase | `TodoForm.tsx` |
| ファイル名（サービス） | PascalCase | `TodoService.ts` |
| ファイル名（型定義） | lowercase | `index.ts` |

### テストファイル命名

| 種類 | 規則 | 例 |
|------|------|-----|
| Python単体テスト | `test_*.py` | `test_models.py`, `test_services.py` |
| TypeScriptテスト | `*.test.tsx/ts` | `TodoForm.test.tsx`, `TodoService.test.ts` |

---

## ドキュメンテーション規約

### Pythonドキュメント

**モジュールレベル**:
```python
"""TODOモデルの定義。

このモジュールは、TODOアプリケーションのコアとなるTODOモデルを定義します。
"""
```

**クラスレベル**:
```python
class Todo(models.Model):
    """TODOアイテムを表すモデル。

    ユーザーのタスク管理を行うためのTODOアイテムを表現します。

    Attributes:
        PRIORITY_LOW (str): 優先度「低」を表す定数
        title (str): TODOのタイトル（最大200文字）
        completed (bool): 完了状態（デフォルト: False）
    """
```

**メソッドレベル**:
```python
def get_todos(
    completed: bool | None = None,
    priority: str | None = None,
) -> QuerySet[Todo]:
    """TODOのクエリセットを取得する。

    完了状態と優先度でフィルタリングしたTODOのクエリセットを返します。

    Args:
        completed (bool | None): 完了状態でフィルタ。Noneの場合は全て取得
        priority (str | None): 優先度でフィルタ。Noneの場合は全て取得

    Returns:
        QuerySet[Todo]: フィルタ済みTODOクエリセット

    Raises:
        ValueError: 優先度が不正な値の場合

    Examples:
        >>> get_todos(completed=True)
        <QuerySet [<Todo: Buy milk>]>
    """
```

**ドキュメントスタイル**: Google Style Docstrings

### TypeScriptドキュメント

**ファイルレベル**:
```typescript
/**
 * @fileoverview TODO作成フォームコンポーネント
 *
 * 新しいTODOを作成するためのフォームを提供します。
 */
```

**インターフェース**:
```typescript
/**
 * TODOフォームのプロパティ
 */
interface TodoFormProps {
  /** フォーム送信時のコールバック関数 */
  onSubmit: (todo: TodoCreate) => void;
  /** キャンセルボタン押下時のコールバック関数（オプション） */
  onCancel?: () => void;
}
```

**関数・コンポーネント**:
```typescript
/**
 * TODO作成フォームコンポーネント
 *
 * 新しいTODOを作成するためのフォームを表示します。
 * タイトル、説明、優先度、期限日を入力できます。
 *
 * @param {TodoFormProps} props - コンポーネントのプロパティ
 * @returns {JSX.Element} TODOフォーム
 */
export default function TodoForm({ onSubmit, onCancel }: TodoFormProps) {
  // 実装
}
```

**ドキュメントスタイル**: JSDoc

---

## テスト規約

### テスト戦略

このプロジェクトでは、以下の3種類のテストを実施します：

1. **ユニットテスト**: 単一の関数・メソッドの動作を検証
2. **統合テスト**: 複数のコンポーネントの連携を検証
3. **スナップショットテスト**: APIレスポンスの一貫性を検証

### バックエンドテスト（pytest）

#### ディレクトリ構造

```
api/tests/
├── conftest.py          # グローバルフィクスチャ
├── unit/                # ユニットテスト
│   ├── test_models.py
│   ├── test_serializers.py
│   └── test_services.py
├── integration/         # 統合テスト
│   └── test_api.py
├── snapshot/            # スナップショットテスト
│   ├── test_todos.py
│   └── README.md
└── fixtures/            # テストヘルパー
    └── snapshot_helpers.py
```

#### テスト命名規則

```python
class TestTodoModel:
    """Todoモデルのテスト"""

    def test_title_boundary_max_length(self):
        """【境界値テスト】タイトルの最大文字数（200文字）

        【テストの意図】
        タイトルが200文字まで正しく保存されることを保証します。

        【何を保証するか】
        - 200文字のタイトルでTODOを作成できること
        - タイトルが200文字として正しく保存されること

        【テスト手順】
        1. 200文字の文字列をタイトルに設定してTODOを作成
        2. 保存されたタイトルの文字数が200であることを確認

        【期待する結果】
        200文字のタイトルが正常に保存される
        """
        max_title = "a" * 200
        todo = Todo.objects.create(title=max_title)
        assert len(todo.title) == 200
```

**テスト命名パターン**:
- `test_<機能>_<条件>`: 例 `test_title_boundary_max_length`
- クラス名: `Test<対象クラス名>`: 例 `TestTodoModel`

#### テスト分類

**良いテスト（Good Examples）**:
- ✅ 境界値テスト（0文字、200文字、201文字）
- ✅ 同値分割（有効値・無効値）
- ✅ ビジネスロジックのテスト
- ✅ エラーハンドリングのテスト

**悪いテスト（Bad Examples）**:
- ❌ 常にパスするテスト（`assert True`）
- ❌ 実装の内部詳細に依存するテスト
- ❌ フレームワークのテスト

**優先度の低いテスト（Low Priority Examples）**:
- 🔻 単純なgetter/setter
- 🔻 `__str__` メソッド
- 🔻 フレームワークが既に保証している動作

#### フィクスチャ（conftest.py）

```python
import pytest
from api.models.todo import Todo

@pytest.fixture
def sample_todo():
    """標準的なTODOのフィクスチャ"""
    return Todo.objects.create(
        title="Sample TODO",
        description="This is a sample TODO",
        priority=Todo.PRIORITY_MEDIUM,
        completed=False,
    )

@pytest.fixture
def multiple_todos():
    """複数のTODO（10件）を作成するフィクスチャ"""
    todos = [
        Todo(
            title=f"TODO {i}",
            priority=[Todo.PRIORITY_LOW, Todo.PRIORITY_MEDIUM, Todo.PRIORITY_HIGH][i % 3],
            completed=i % 2 == 0,
        )
        for i in range(10)
    ]
    return Todo.objects.bulk_create(todos)

@pytest.fixture
def api_client():
    """DRF APIクライアントのフィクスチャ"""
    from rest_framework.test import APIClient
    return APIClient()
```

#### スナップショットテスト

**目的**: APIレスポンスの一貫性を保証

**仕組み**:
1. Parquet形式でゴールデンデータを保存
2. APIレスポンスとゴールデンデータを比較
3. 差分があればテスト失敗

**使用例**:
```python
@pytest.mark.snapshot
def test_all_todos_snapshot(api_client, setup_golden_data):
    """全TODO取得APIのレスポンスがゴールデンデータと一致する"""
    response = api_client.get("/api/todos/")
    data = response.json()

    snapshot_comparator.assert_matches_snapshot(
        data,
        "todos_all",
        exclude_fields=["id", "created_at", "updated_at"],
    )
```

#### テスト実行コマンド

```bash
# 全テスト実行
pytest

# ユニットテストのみ
pytest api/tests/unit/

# 統合テストのみ
pytest api/tests/integration/

# カバレッジ付き実行
pytest --cov=api --cov-report=html

# 特定のマーカーを除外
pytest --ignore=api/tests/snapshot
```

#### カバレッジ目標

- **全体**: 90%以上
- **models**: 95%以上
- **serializers**: 90%以上
- **services**: 95%以上
- **views**: 85%以上

### フロントエンドテスト（Vitest + Testing Library）

#### ディレクトリ構造

```
tests/
├── setup/
│   └── setupTests.ts    # テストセットアップ
└── unit/
    ├── components/      # コンポーネントテスト
    │   ├── TodoForm.test.tsx
    │   ├── TodoList.test.tsx
    │   └── TodoItem.test.tsx
    └── services/        # サービステスト
        └── TodoService.test.ts
```

#### テスト命名規則

```typescript
describe("TodoForm - Good Examples", () => {
  it("renders all form fields", () => {
    /**
     * 【テストの意図】
     * フォームコンポーネントが必要なすべてのフィールドを表示することを保証します。
     *
     * 【何を保証するか】
     * - タイトル入力フィールドが表示されること
     * - 説明入力フィールドが表示されること
     * - 優先度選択フィールドが表示されること
     * - 作成ボタンが表示されること
     *
     * 【テスト手順】
     * 1. TodoFormコンポーネントをレンダリング
     * 2. 各フィールドとボタンがDOMに存在することを確認
     *
     * 【期待する結果】
     * すべてのフィールドとボタンがDOMに存在する
     */
    render(<TodoForm onSubmit={vi.fn()} />);

    expect(screen.getByLabelText(/タイトル/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/説明/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/優先度/i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /作成/i })).toBeInTheDocument();
  });

  it("calls onSubmit with form data when submitted", async () => {
    /**
     * 【テストの意図】
     * フォーム送信時に正しいデータでonSubmitが呼ばれることを保証します。
     */
    const handleSubmit = vi.fn();
    render(<TodoForm onSubmit={handleSubmit} />);

    const user = userEvent.setup();

    await user.type(screen.getByLabelText(/タイトル/i), "New TODO");
    await user.click(screen.getByRole("button", { name: /作成/i }));

    expect(handleSubmit).toHaveBeenCalledWith({
      title: "New TODO",
      description: "",
      priority: "medium",
      due_date: null,
    });
  });
});
```

#### テスト実行コマンド

```bash
# 全テスト実行
npm test

# ウォッチモード
npm run test:watch

# カバレッジ付き実行
npm run test:coverage

# UIモード
npm run test:ui
```

#### カバレッジ目標

- **全体**: 80%以上
- **components**: 85%以上
- **services**: 90%以上

---

## リンター・フォーマッタ設定

### バックエンド: Ruff

**設定ファイル**: `backend/pyproject.toml`

```toml
[tool.ruff]
line-length = 88
target-version = "py311"
extend-exclude = ["migrations"]

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
    "UP",  # pyupgrade
]
ignore = []

[tool.ruff.lint.isort]
known-first-party = ["api", "config"]
```

**実行コマンド**:
```bash
# Lint実行
ruff check .

# 自動修正
ruff check --fix .

# フォーマット
ruff format .
```

### フロントエンド: Biome

**設定ファイル**: `frontend/biome.json`

```json
{
  "$schema": "https://biomejs.dev/schemas/1.9.4/schema.json",
  "vcs": {
    "enabled": true,
    "clientKind": "git",
    "useIgnoreFile": true
  },
  "files": {
    "ignoreUnknown": false,
    "ignore": ["dist", "build", "node_modules", "coverage", ".vite"]
  },
  "formatter": {
    "enabled": true,
    "indentStyle": "space",
    "indentWidth": 2,
    "lineWidth": 100
  },
  "organizeImports": {
    "enabled": true
  },
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true,
      "correctness": {
        "noUnusedVariables": "error",
        "useExhaustiveDependencies": "warn"
      },
      "style": {
        "noNonNullAssertion": "warn"
      }
    }
  },
  "javascript": {
    "formatter": {
      "quoteStyle": "double",
      "semicolons": "always"
    }
  }
}
```

**実行コマンド**:
```bash
# Lint + Format チェック
npm run lint

# 自動修正
npm run lint:fix

# フォーマットのみ
npm run format
```

---

## pre-commit設定

### ルートレベル設定

**ファイル**: `.pre-commit-config.yaml`

```yaml
repos:
  # バックエンド（Ruff）
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.14.5
    hooks:
      - id: ruff
        args: [--fix]
        files: ^backend/
      - id: ruff-format
        files: ^backend/

  # フロントエンド（Biome）
  - repo: https://github.com/biomejs/pre-commit
    rev: v0.6.0
    hooks:
      - id: biome-check
        files: ^frontend/
        additional_dependencies: ["@biomejs/biome@1.9.4"]

  # 共通チェック
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: check-yaml
      - id: check-json
      - id: end-of-file-fixer
      - id: trailing-whitespace
      - id: check-added-large-files
        args: ["--maxkb=1000"]
      - id: check-merge-conflict
      - id: detect-private-key
```

### バックエンド専用設定

**ファイル**: `backend/.pre-commit-config.yaml`

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-toml
      - id: check-added-large-files

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.14.5
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

### フロントエンド（Husky）

**ファイル**: `frontend/.husky/pre-commit`

```bash
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

cd frontend && npm run lint
```

### インストール・実行

```bash
# インストール
pre-commit install

# 手動実行（全ファイル）
pre-commit run --all-files

# 手動実行（特定ファイル）
pre-commit run --files backend/api/models/todo.py
```

---

## Git規約

### コミットメッセージ

**フォーマット**:
```
<type>: <subject>

<body>

<footer>
```

**Type**:
- `feat`: 新機能
- `fix`: バグ修正
- `docs`: ドキュメントのみの変更
- `style`: コードの動作に影響しない変更（フォーマット、セミコロン等）
- `refactor`: バグ修正や機能追加を含まないコード変更
- `test`: テストの追加・修正
- `chore`: ビルドプロセスやツールの変更

**例**:
```
feat: TODOの優先度フィルタリング機能を追加

優先度（low/medium/high）でTODOをフィルタリングできる機能を実装。
APIエンドポイント、サービス層、フロントエンドコンポーネントを追加。

Closes #123
```

### ブランチ戦略

**ブランチ命名規則**:
- `main`: 本番環境
- `develop`: 開発環境
- `feature/<機能名>`: 新機能開発
- `fix/<バグ名>`: バグ修正
- `docs/<ドキュメント名>`: ドキュメント更新

**例**:
```
feature/todo-priority-filter
fix/todo-date-validation
docs/api-documentation
```

### Pull Request

**PRテンプレート**:
```markdown
## 概要
変更内容の概要を記載

## 変更内容
- 変更点1
- 変更点2

## テスト
- [ ] ユニットテスト追加
- [ ] 統合テスト追加
- [ ] 手動テスト完了

## スクリーンショット（該当する場合）

## 関連Issue
Closes #123
```

---

## IDE設定（VSCode）

### 推奨拡張機能

**ファイル**: `.vscode/extensions.json`

```json
{
  "recommendations": [
    "charliermarsh.ruff",
    "ms-python.python",
    "ms-python.vscode-pylance",
    "biomejs.biome",
    "bradlc.vscode-tailwindcss",
    "dbaeumer.vscode-eslint"
  ]
}
```

### ワークスペース設定

**ファイル**: `.vscode/settings.json`

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/backend/.venv/bin/python",
  "python.analysis.extraPaths": ["${workspaceFolder}/backend"],
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": ["backend/api/tests"],

  "[python]": {
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.organizeImports": "explicit",
      "source.fixAll": "explicit"
    },
    "editor.defaultFormatter": "charliermarsh.ruff"
  },

  "[typescript]": {
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.organizeImports": "explicit",
      "source.fixAll": "explicit"
    },
    "editor.defaultFormatter": "biomejs.biome"
  },

  "[typescriptreact]": {
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.organizeImports": "explicit",
      "source.fixAll": "explicit"
    },
    "editor.defaultFormatter": "biomejs.biome"
  },

  "files.exclude": {
    "**/__pycache__": true,
    "**/*.pyc": true,
    "**/node_modules": true,
    "**/.venv": true
  },

  "ruff.configurationPreference": "editorFirst",
  "ruff.lineLength": 88
}
```

**重要な設定**:
1. **保存時自動フォーマット**: `editor.formatOnSave: true`
2. **保存時インポート整理**: `source.organizeImports: "explicit"`
3. **Pythonフォーマッタ**: Ruff
4. **TypeScriptフォーマッタ**: Biome

---

## CI/CD規約

### GitHub Actions（準備中）

**想定ワークフロー**:

1. **Pull Request時**:
   - Lint・Format チェック
   - ユニットテスト実行
   - カバレッジ計測

2. **main ブランチマージ時**:
   - 統合テスト実行
   - ビルド
   - デプロイ（該当する場合）

**設定例（`.github/workflows/test.yml`）**:
```yaml
name: Test

on:
  pull_request:
    branches: [main, develop]
  push:
    branches: [main, develop]

jobs:
  backend-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          cd backend
          pip install uv
          uv pip install -e ".[dev]"
      - name: Run tests
        run: |
          cd backend
          pytest --cov=api --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          file: ./backend/coverage.xml

  frontend-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - name: Install dependencies
        run: |
          cd frontend
          npm ci
      - name: Run tests
        run: |
          cd frontend
          npm run test:coverage
      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          file: ./frontend/coverage/coverage-final.json
```

---

## 依存関係管理規約

### バックエンド（uv）

**管理ファイル**:
- `pyproject.toml`: 依存関係定義
- `uv.lock`: ロックファイル（バージョン固定）

**依存関係追加**:
```bash
# 本番依存関係
uv pip install <package>

# 開発依存関係
# pyproject.toml の [project.optional-dependencies] dev に手動で追加
uv pip install -e ".[dev]"
```

**更新**:
```bash
# 全依存関係更新
uv pip install --upgrade -e ".[dev]"
```

**pyproject.toml 構成**:
```toml
[project]
requires-python = ">=3.11"
dependencies = [
    "django>=5.2.8",
    "djangorestframework>=3.16.1",
    # ...
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "ruff>=0.14.4",
    # ...
]
```

### フロントエンド（npm）

**管理ファイル**:
- `package.json`: 依存関係定義
- `package-lock.json`: ロックファイル（バージョン固定）

**依存関係追加**:
```bash
# 本番依存関係
npm install <package>

# 開発依存関係
npm install --save-dev <package>
```

**更新**:
```bash
# 全依存関係更新
npm update

# 特定パッケージ更新
npm update <package>
```

**package.json 構成**:
```json
{
  "dependencies": {
    "react": "^18.3.1",
    "date-fns": "^3.0.0"
  },
  "devDependencies": {
    "@biomejs/biome": "^2.2.5",
    "vitest": "^4.0.10"
  }
}
```

---

## まとめ

このコーディング規約を遵守することで、以下が保証されます：

1. **一貫性**: 全ての開発者が同じスタイルでコードを記述
2. **可読性**: コードの意図が明確で理解しやすい
3. **保守性**: 変更・拡張が容易で、バグが混入しにくい
4. **品質**: テストとリンターにより高品質を維持
5. **効率**: 自動化ツールにより開発速度を向上

規約に関する疑問点や改善提案がある場合は、チームで議論してください。

---

**参考リンク**:
- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [React Documentation](https://react.dev/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [Biome Documentation](https://biomejs.dev/)
- [pytest Documentation](https://docs.pytest.org/)
- [Vitest Documentation](https://vitest.dev/)
