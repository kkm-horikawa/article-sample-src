"""TODOサービスレイヤーの定義。

このモジュールは、TODOに関するビジネスロジックを提供します。
データベース操作をカプセル化し、再利用可能なサービスメソッドを提供します。
"""

from datetime import date

from django.db.models import Q, QuerySet

from api.models.todo import Todo


class TodoService:
    """TODOのビジネスロジックを提供するサービスクラス。

    データベース操作を抽象化し、TODOの検索、作成、更新、削除などの
    ビジネスロジックを提供します。すべてのメソッドは静的メソッドです。
    """

    @staticmethod
    def get_todos(
        completed: bool | None = None,
        priority: str | None = None,
        overdue_only: bool = False,
    ) -> QuerySet[Todo]:
        """TODO一覧を取得する。

        指定されたフィルタ条件に基づいてTODOを検索します。
        複数の条件を組み合わせてフィルタリングできます。

        Args:
            completed (bool | None): 完了状態でフィルタ
                - True: 完了済みのTODOのみ
                - False: 未完了のTODOのみ
                - None: すべてのTODO（デフォルト）
            priority (str | None): 優先度でフィルタ
                - "low", "medium", "high" のいずれか
                - None: すべての優先度（デフォルト）
            overdue_only (bool): 期限切れのTODOのみを取得するか
                - True: 期限切れかつ未完了のTODOのみ
                - False: フィルタなし（デフォルト）

        Returns:
            QuerySet[Todo]: フィルタリングされたTODOのクエリセット
        """
        queryset = Todo.objects.all()

        if completed is not None:
            queryset = queryset.filter(completed=completed)

        if priority:
            queryset = queryset.filter(priority=priority)

        if overdue_only:
            today = date.today()
            queryset = queryset.filter(Q(due_date__lt=today) & Q(completed=False))

        return queryset

    @staticmethod
    def create_todo(
        title: str,
        description: str = "",
        priority: str = Todo.PRIORITY_MEDIUM,
        due_date: date | None = None,
    ) -> Todo:
        """新しいTODOを作成する。

        指定されたパラメータで新しいTODOをデータベースに作成します。

        Args:
            title (str): TODOのタイトル
            description (str): TODOの説明（デフォルト: 空文字列）
            priority (str): 優先度（デフォルト: medium）
            due_date (date | None): 期限日（デフォルト: None）

        Returns:
            Todo: 作成されたTODOインスタンス
        """
        todo = Todo.objects.create(
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
        )
        return todo

    @staticmethod
    def toggle_completed(todo: Todo) -> Todo:
        """TODOの完了状態を切り替える。

        未完了のTODOは完了に、完了済みのTODOは未完了に状態を変更します。

        Args:
            todo (Todo): 状態を切り替えるTODOインスタンス

        Returns:
            Todo: 更新されたTODOインスタンス
        """
        todo.completed = not todo.completed
        todo.save()
        return todo

    @staticmethod
    def bulk_delete_completed() -> int:
        """完了済みのTODOを一括削除する。

        完了状態のTODOをすべて削除します。

        Returns:
            int: 削除されたTODOの件数
        """
        count, _ = Todo.objects.filter(completed=True).delete()
        return count

    @staticmethod
    def get_statistics():
        """TODOの統計情報を取得する。

        全体の件数、完了済み件数、未完了件数、期限切れ件数を集計します。

        Returns:
            dict: 以下のキーを持つ統計情報の辞書
                - total (int): 全TODO件数
                - completed (int): 完了済みTODO件数
                - pending (int): 未完了TODO件数
                - overdue (int): 期限切れTODO件数
        """
        total = Todo.objects.count()
        completed = Todo.objects.filter(completed=True).count()
        pending = total - completed
        overdue = Todo.objects.filter(
            Q(due_date__lt=date.today()) & Q(completed=False)
        ).count()

        return {
            "total": total,
            "completed": completed,
            "pending": pending,
            "overdue": overdue,
        }
