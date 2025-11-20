"""Django 管理サイトの設定モジュール。

TODO モデルの管理画面のカスタマイズを定義します。
"""

from django.contrib import admin

from api.models.todo import Todo


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    """TODO モデルの管理画面設定。

    管理画面での TODO の表示、フィルタリング、検索機能をカスタマイズします。

    Attributes:
        list_display: 一覧画面に表示するフィールド
        list_filter: サイドバーに表示するフィルタ
        search_fields: 検索対象のフィールド
        date_hierarchy: 日付階層ナビゲーションのフィールド
    """

    list_display = ["id", "title", "priority", "completed", "due_date", "created_at"]
    list_filter = ["completed", "priority", "created_at"]
    search_fields = ["title", "description"]
    date_hierarchy = "created_at"
