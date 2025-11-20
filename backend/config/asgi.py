"""ASGI 設定モジュール。

このモジュールは、ASGI サーバー（例: Uvicorn, Daphne）で
Django アプリケーションを実行するための ASGI アプリケーションを定義します。

ASGI (Asynchronous Server Gateway Interface) は、非同期対応の
Python Web アプリケーションと Web サーバー間の標準インターフェースです。
WebSocket や HTTP/2 などの非同期プロトコルをサポートします。
"""

import os

from django.core.asgi import get_asgi_application

# Django 設定モジュールの環境変数を設定
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# ASGI アプリケーションを取得
application = get_asgi_application()
