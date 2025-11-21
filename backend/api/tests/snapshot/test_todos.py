"""TODOエンドポイントのスナップショットテスト。

このモジュールは、TODO APIエンドポイントのレスポンスを
ゴールデンデータ（Parquet形式）と比較するスナップショットテストを実施します。
APIレスポンスの構造と内容が期待通りであることを保証します。
"""

from datetime import date, timedelta
from pathlib import Path

import pytest

from api.models.todo import Todo
from api.tests.fixtures.snapshot_helpers import GoldenDataLoader, SnapshotComparator

DATA_DIR = Path(__file__).parent.parent / "data" / "golden"
golden_loader = GoldenDataLoader(DATA_DIR)
snapshot_comparator = SnapshotComparator(golden_loader)


@pytest.fixture
def setup_golden_data():
    """スナップショットテスト用のゴールデンデータをセットアップするフィクスチャ。

    3件のTODO（高優先度・未完了、中優先度・未完了、低優先度・完了）を作成し、
    テスト終了後にクリーンアップします。

    Yields:
        None: セットアップ完了後、テストに制御を渡す
    """
    Todo.objects.all().delete()

    todos_data = [
        {
            "title": "Buy groceries",
            "description": "Milk, eggs, bread",
            "priority": "high",
            "completed": False,
            "due_date": date.today() + timedelta(days=1),
        },
        {
            "title": "Write report",
            "description": "Q4 sales report",
            "priority": "medium",
            "completed": False,
            "due_date": date.today() + timedelta(days=7),
        },
        {
            "title": "Clean room",
            "description": "",
            "priority": "low",
            "completed": True,
            "due_date": None,
        },
    ]

    for todo_data in todos_data:
        Todo.objects.create(**todo_data)

    yield

    Todo.objects.all().delete()


@pytest.mark.django_db
@pytest.mark.snapshot
class TestTodoSnapshotsGoodExamples:
    """TODOエンドポイントのスナップショットテスト（良いテスト例）。

    ゴールデンデータを使用してAPIレスポンスの一貫性を検証します。
    """

    def test_all_todos_snapshot(self, api_client, setup_golden_data):
        """全TODO取得APIのレスポンスがゴールデンデータと一致することを確認する。

        【テストの意図】
        全TODO取得APIのレスポンス構造と内容が
        ゴールデンデータ（Parquetファイル）と一致することを保証します。

        【何を保証するか】
        - ステータスコードが200であること
        - レスポンスデータが todos_all.parquet と一致すること
        - id, created_at, updated_at 以外のフィールドが完全一致すること

        【テスト手順】
        1. setup_golden_data フィクスチャで3件のTODOを作成
        2. GET /api/todos/ を実行
        3. ステータスコード200を確認
        4. レスポンスデータとゴールデンデータを比較

        【期待する結果】
        レスポンスデータがゴールデンデータと完全に一致すること
        """
        response = api_client.get("/api/todos/")

        assert response.status_code == 200
        data = response.json()

        snapshot_comparator.assert_matches_snapshot(
            data,
            "todos_all",
            exclude_fields=["id", "created_at", "updated_at"],
        )

    def test_completed_todos_snapshot(self, api_client, setup_golden_data):
        """完了済みTODO取得APIのレスポンスがゴールデンデータと一致することを確認する。

        【テストの意図】
        completed=true フィルタを使用したTODO取得APIのレスポンスが
        ゴールデンデータと一致することを保証します。

        【何を保証するか】
        - ステータスコードが200であること
        - completed=true でフィルタされたレスポンスデータが
          todos_completed.parquet と一致すること
        - 完了済みTODOのみが返されること

        【テスト手順】
        1. setup_golden_data フィクスチャで3件のTODO（1件完了済み）を作成
        2. GET /api/todos/?completed=true を実行
        3. ステータスコード200を確認
        4. レスポンスデータとゴールデンデータを比較

        【期待する結果】
        完了済みTODO（Clean room）のみがゴールデンデータと一致して返されること
        """
        response = api_client.get("/api/todos/?completed=true")

        assert response.status_code == 200
        data = response.json()

        snapshot_comparator.assert_matches_snapshot(
            data,
            "todos_completed",
            exclude_fields=["id", "created_at", "updated_at"],
        )

    def test_high_priority_todos_snapshot(self, api_client, setup_golden_data):
        """高優先度TODO取得APIのレスポンスがゴールデンデータと一致することを確認する。

        【テストの意図】
        priority=high フィルタを使用したTODO取得APIのレスポンスが
        ゴールデンデータと一致することを保証します。

        【何を保証するか】
        - ステータスコードが200であること
        - priority=high でフィルタされたレスポンスデータが
          todos_high_priority.parquet と一致すること
        - 高優先度TODOのみが返されること

        【テスト手順】
        1. setup_golden_data フィクスチャで3件のTODO（1件高優先度）を作成
        2. GET /api/todos/?priority=high を実行
        3. ステータスコード200を確認
        4. レスポンスデータとゴールデンデータを比較

        【期待する結果】
        高優先度TODO（Buy groceries）のみがゴールデンデータと一致して返されること
        """
        response = api_client.get("/api/todos/?priority=high")

        assert response.status_code == 200
        data = response.json()

        snapshot_comparator.assert_matches_snapshot(
            data,
            "todos_high_priority",
            exclude_fields=["id", "created_at", "updated_at"],
        )
