"""TODOビューセットの定義。

このモジュールは、TODO APIのエンドポイントを提供するビューセットを定義します。
"""

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.endpoints.todos.serializers import TodoSerializer
from api.endpoints.todos.services import TodoService
from api.models.todo import Todo


class TodoViewSet(viewsets.ModelViewSet):
    """TODO APIのビューセット。

    TODOのCRUD操作と追加のカスタムアクションを提供します。
    DRFのModelViewSetを継承し、標準的なREST APIエンドポイントを自動生成します。

    提供するエンドポイント:
        - GET /api/todos/ - TODO一覧取得
        - POST /api/todos/ - TODO作成
        - GET /api/todos/{id}/ - TODO詳細取得
        - PUT /api/todos/{id}/ - TODO更新
        - PATCH /api/todos/{id}/ - TODO部分更新
        - DELETE /api/todos/{id}/ - TODO削除
        - POST /api/todos/{id}/toggle/ - 完了状態切り替え
        - DELETE /api/todos/bulk_delete_completed/ - 完了済み一括削除
        - GET /api/todos/statistics/ - 統計情報取得
    """

    serializer_class = TodoSerializer
    queryset = Todo.objects.all()

    def get_queryset(self):
        """TODOのクエリセットを取得する。

        リクエストのクエリパラメータに基づいてフィルタリングされた
        TODOのクエリセットを返します。

        クエリパラメータ:
            - completed (bool): 完了状態でフィルタ（true/false）
            - priority (str): 優先度でフィルタ（low/medium/high）
            - overdue_only (bool): 期限切れのみ取得（true）

        Returns:
            QuerySet[Todo]: フィルタリングされたTODOのクエリセット
        """
        completed = self.request.query_params.get("completed")
        priority = self.request.query_params.get("priority")
        overdue_only = self.request.query_params.get("overdue_only") == "true"

        if completed is not None:
            completed = completed.lower() == "true"

        return TodoService.get_todos(
            completed=completed, priority=priority, overdue_only=overdue_only
        )

    @action(detail=True, methods=["post"])
    def toggle(self, request, pk=None):
        """TODOの完了状態を切り替える。

        指定されたTODOの完了状態を反転させます（完了⇔未完了）。

        Args:
            request: HTTPリクエストオブジェクト
            pk: TODOのID

        Returns:
            Response: 更新されたTODOのJSONレスポンス
        """
        todo = self.get_object()
        updated_todo = TodoService.toggle_completed(todo)
        serializer = self.get_serializer(updated_todo)
        return Response(serializer.data)

    @action(detail=False, methods=["delete"])
    def bulk_delete_completed(self, request):
        """完了済みのTODOを一括削除する。

        完了状態のTODOをすべて削除します。

        Args:
            request: HTTPリクエストオブジェクト

        Returns:
            Response: 削除件数を含むJSONレスポンス
        """
        count = TodoService.bulk_delete_completed()
        return Response({"deleted_count": count})

    @action(detail=False, methods=["get"])
    def statistics(self, request):
        """TODOの統計情報を取得する。

        全体件数、完了済み件数、未完了件数、期限切れ件数を取得します。

        Args:
            request: HTTPリクエストオブジェクト

        Returns:
            Response: 統計情報を含むJSONレスポンス
        """
        stats = TodoService.get_statistics()
        return Response(stats)
