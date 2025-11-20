#!/usr/bin/env python
"""Django 管理コマンドのエントリーポイント。

このスクリプトは、Django の管理コマンド（migrate, runserver, test など）を
実行するためのエントリーポイントです。
"""

import os
import sys


def main():
    """Django 管理コマンドを実行する。

    環境変数 DJANGO_SETTINGS_MODULE を設定し、
    Django のコマンドラインユーティリティを実行します。

    Raises:
        ImportError: Django がインストールされていない場合
    """
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
