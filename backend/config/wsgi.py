"""WSGI 設定モジュール。

このモジュールは、WSGI サーバー（例: Gunicorn, uWSGI）で
Django アプリケーションを実行するための WSGI アプリケーションを定義します。

WSGI (Web Server Gateway Interface) は、Python Web アプリケーションと
Web サーバー間の標準インターフェースです。
"""

import os

from django.core.wsgi import get_wsgi_application

# Django 設定モジュールの環境変数を設定
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# WSGI アプリケーションを取得
application = get_wsgi_application()
