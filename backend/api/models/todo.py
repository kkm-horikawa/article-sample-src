"""TODOモデルの定義。

このモジュールは、TODOアプリケーションのコアとなるTODOモデルを定義します。
"""

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Todo(models.Model):
    """TODOアイテムを表すモデル。

    ユーザーのタスク管理を行うためのTODOアイテムを表現します。
    タイトル、説明、優先度、期限、完了状態などの情報を保持します。

    Attributes:
        PRIORITY_LOW (str): 優先度「低」を表す定数
        PRIORITY_MEDIUM (str): 優先度「中」を表す定数
        PRIORITY_HIGH (str): 優先度「高」を表す定数
        title (str): TODOのタイトル（最大200文字）
        description (str): TODOの詳細説明（任意）
        completed (bool): 完了状態（デフォルト: False）
        priority (str): 優先度（low/medium/high、デフォルト: medium）
        due_date (date): 期限日（任意）
        created_at (datetime): 作成日時（自動設定）
        updated_at (datetime): 更新日時（自動更新）
    """

    PRIORITY_LOW = "low"
    PRIORITY_MEDIUM = "medium"
    PRIORITY_HIGH = "high"

    PRIORITY_CHOICES = [
        (PRIORITY_LOW, "Low"),
        (PRIORITY_MEDIUM, "Medium"),
        (PRIORITY_HIGH, "High"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=10, choices=PRIORITY_CHOICES, default=PRIORITY_MEDIUM
    )
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "todos"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["completed"]),
            models.Index(fields=["priority"]),
            models.Index(fields=["due_date"]),
        ]

    def __str__(self):
        return self.title

    def clean(self):
        """モデルのバリデーションを実行する。

        期限日が過去の日付でないことを検証します。

        Raises:
            ValidationError: 期限日が過去の日付の場合
        """
        if self.due_date and self.due_date < timezone.now().date():
            raise ValidationError({"due_date": "Due date cannot be in the past"})

    def is_overdue(self):
        """TODOが期限切れかどうかを判定する。

        期限日が設定されており、かつ未完了で、期限日が過去の場合にTrueを返します。
        完了済みのTODOや期限日が未設定のTODOは期限切れと判定しません。

        Returns:
            bool: 期限切れの場合True、それ以外はFalse
        """
        if not self.due_date or self.completed:
            return False
        return self.due_date < timezone.now().date()

    def get_priority_display_ja(self):
        """優先度の日本語表記を取得する。

        優先度の値（low/medium/high）を日本語（低/中/高）に変換して返します。

        Returns:
            str: 優先度の日本語表記（該当なしの場合は空文字列）
        """
        priority_ja = {
            self.PRIORITY_LOW: "低",
            self.PRIORITY_MEDIUM: "中",
            self.PRIORITY_HIGH: "高",
        }
        return priority_ja.get(self.priority, "")
