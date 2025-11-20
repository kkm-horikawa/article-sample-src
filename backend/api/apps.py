"""API アプリケーションの設定モジュール。

このモジュールは、Django アプリケーション 'api' の設定を定義します。
"""

from django.apps import AppConfig


class ApiConfig(AppConfig):
    """API アプリケーションの設定クラス。

    Attributes:
        default_auto_field: モデルの主キーに使用するフィールドタイプ
        name: アプリケーション名
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "api"
