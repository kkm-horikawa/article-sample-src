"""TODOシリアライザーの定義。

このモジュールは、TODO APIのリクエスト/レスポンスデータを
シリアライズ/デシリアライズするためのシリアライザーを提供します。
"""

from rest_framework import serializers

from api.models.todo import Todo


class TodoSerializer(serializers.ModelSerializer):
    """TODOモデルのシリアライザー。

    TODOモデルのインスタンスをJSON形式に変換し、また逆にJSON形式のデータから
    TODOモデルのインスタンスを生成します。バリデーションも行います。

    Attributes:
        is_overdue (BooleanField): 期限切れ判定（読み取り専用）
        priority_display_ja (CharField): 優先度の日本語表記（読み取り専用）
    """

    is_overdue = serializers.BooleanField(read_only=True)
    priority_display_ja = serializers.CharField(
        source="get_priority_display_ja", read_only=True
    )

    class Meta:
        model = Todo
        fields = [
            "id",
            "title",
            "description",
            "completed",
            "priority",
            "priority_display_ja",
            "due_date",
            "is_overdue",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_title(self, value):
        """タイトルのバリデーションを行う。

        タイトルが空文字列や空白のみでないこと、200文字以内であることを検証します。
        また、前後の空白を除去した値を返します。

        Args:
            value (str): バリデーション対象のタイトル

        Returns:
            str: 前後の空白を除去したタイトル

        Raises:
            ValidationError: タイトルが空または200文字を超える場合
        """
        if not value or not value.strip():
            raise serializers.ValidationError("Title cannot be empty")
        if len(value) > 200:
            raise serializers.ValidationError("Title must be 200 characters or less")
        return value.strip()

    def validate_priority(self, value):
        """優先度のバリデーションを行う。

        優先度が有効な値（low/medium/high）のいずれかであることを検証します。

        Args:
            value (str): バリデーション対象の優先度

        Returns:
            str: バリデーション済みの優先度

        Raises:
            ValidationError: 優先度が有効な値でない場合
        """
        valid_priorities = [Todo.PRIORITY_LOW, Todo.PRIORITY_MEDIUM, Todo.PRIORITY_HIGH]
        if value not in valid_priorities:
            raise serializers.ValidationError(
                f"Priority must be one of {', '.join(valid_priorities)}"
            )
        return value
