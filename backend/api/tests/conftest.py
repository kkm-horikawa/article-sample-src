"""pytestフィクスチャの定義。

このモジュールは、テストで使用する共通のフィクスチャを定義します。
様々なTODOのテストデータやAPIクライアントを提供します。
"""

from datetime import timedelta

import pytest
from django.utils import timezone

from api.models.todo import Todo


@pytest.fixture
def sample_todo():
    """標準的なTODOのフィクスチャ。

    Returns:
        Todo: 未完了の中優先度TODO
    """
    return Todo.objects.create(
        title="Sample TODO",
        description="This is a sample TODO",
        priority=Todo.PRIORITY_MEDIUM,
        completed=False,
    )


@pytest.fixture
def completed_todo():
    """完了済みTODOのフィクスチャ。

    Returns:
        Todo: 完了済みの低優先度TODO
    """
    return Todo.objects.create(
        title="Completed TODO",
        description="This is completed",
        priority=Todo.PRIORITY_LOW,
        completed=True,
    )


@pytest.fixture
def overdue_todo():
    """期限切れTODOのフィクスチャ。

    Returns:
        Todo: 昨日が期限の未完了TODO
    """
    yesterday = timezone.now().date() - timedelta(days=1)
    return Todo.objects.create(
        title="Overdue TODO",
        description="This is overdue",
        priority=Todo.PRIORITY_HIGH,
        completed=False,
        due_date=yesterday,
    )


@pytest.fixture
def future_todo():
    """将来期限のTODOフィクスチャ。

    Returns:
        Todo: 明日が期限の未完了TODO
    """
    tomorrow = timezone.now().date() + timedelta(days=1)
    return Todo.objects.create(
        title="Future TODO",
        description="This is in the future",
        priority=Todo.PRIORITY_MEDIUM,
        completed=False,
        due_date=tomorrow,
    )


@pytest.fixture
def multiple_todos():
    """複数のTODOを作成するフィクスチャ。

    10件のTODOを作成します（優先度と完了状態がバラバラ）。

    Returns:
        list[Todo]: 10件のTODOリスト
    """
    todos = [
        Todo(
            title=f"TODO {i}",
            description=f"Description {i}",
            priority=[Todo.PRIORITY_LOW, Todo.PRIORITY_MEDIUM, Todo.PRIORITY_HIGH][
                i % 3
            ],
            completed=i % 2 == 0,
        )
        for i in range(10)
    ]
    return Todo.objects.bulk_create(todos)


@pytest.fixture
def boundary_title_todos():
    """境界値テスト用のTODOフィクスチャ。

    タイトル長の境界値（空、1文字、199文字、200文字）のTODOを作成します。

    Returns:
        list[Todo]: 境界値テスト用TODO4件のリスト
    """
    return [
        Todo.objects.create(title="", description="Empty title"),
        Todo.objects.create(title="A", description="1 character"),
        Todo.objects.create(title="A" * 200, description="200 characters"),
        Todo.objects.create(title="A" * 199, description="199 characters"),
    ]


@pytest.fixture
def all_priority_todos():
    """全優先度のTODOフィクスチャ。

    低・中・高の3つの優先度のTODOを作成します。

    Returns:
        list[Todo]: 各優先度のTODO3件のリスト
    """
    return [
        Todo.objects.create(title="Low", priority=Todo.PRIORITY_LOW),
        Todo.objects.create(title="Medium", priority=Todo.PRIORITY_MEDIUM),
        Todo.objects.create(title="High", priority=Todo.PRIORITY_HIGH),
    ]


@pytest.fixture
def api_client():
    """DRF APIクライアントのフィクスチャ。

    Returns:
        APIClient: DRFのテスト用APIクライアント
    """
    from rest_framework.test import APIClient

    return APIClient()
