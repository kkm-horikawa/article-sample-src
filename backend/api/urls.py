"""API アプリケーションの URL 設定モジュール。

このモジュールは、API エンドポイントのルーティングを定義します。
Django REST Framework の DefaultRouter を使用して、
TODO ViewSet のエンドポイントを自動的に生成します。
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.endpoints.todos.views import TodoViewSet

# DRF のルーターを使用して ViewSet を登録
router = DefaultRouter()
router.register(r"todos", TodoViewSet, basename="todo")

# URL パターンの定義
# ルーターが生成する TODO エンドポイント:
# - GET    /api/todos/          - TODO 一覧取得
# - POST   /api/todos/          - TODO 作成
# - GET    /api/todos/{id}/     - TODO 詳細取得
# - PATCH  /api/todos/{id}/     - TODO 更新
# - DELETE /api/todos/{id}/     - TODO 削除
# - POST   /api/todos/{id}/toggle/ - TODO 完了状態切り替え
# - GET    /api/todos/statistics/   - TODO 統計情報取得
# - DELETE /api/todos/bulk_delete_completed/ - 完了済み TODO 一括削除
urlpatterns = [
    path("", include(router.urls)),
]
