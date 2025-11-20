"""Django プロジェクトの設定モジュール。

TODO アプリケーションの Django 設定を定義します。
開発環境向けの設定が含まれています。

主要な設定:
    - データベース: SQLite3
    - 言語: 日本語
    - タイムゾーン: Asia/Tokyo
    - REST Framework: ページネーション、JSONレンダラー
    - CORS: 全てのオリジンを許可（開発用）
    - API ドキュメント: drf-spectacular

注意:
    本番環境では SECRET_KEY、DEBUG、ALLOWED_HOSTS、CORS 設定を
    適切に変更する必要があります。
"""

from pathlib import Path

# ベースディレクトリのパス
BASE_DIR = Path(__file__).resolve().parent.parent

# セキュリティキー（本番環境では変更必須）
SECRET_KEY = "django-insecure-dev-key-change-in-production"

# デバッグモード（本番環境では False に設定）
DEBUG = True

# 許可するホスト（本番環境では適切に設定）
ALLOWED_HOSTS = ["*"]

# インストール済みアプリケーション
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "drf_spectacular",
    "corsheaders",
    "api",
]

# ミドルウェア
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ルート URL 設定
ROOT_URLCONF = "config.urls"

# テンプレート設定
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# WSGI アプリケーション
WSGI_APPLICATION = "config.wsgi.application"

# データベース設定（SQLite3 を使用）
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# パスワードバリデーション
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation"
            ".UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": ("django.contrib.auth.password_validation.MinimumLengthValidator"),
    },
    {
        "NAME": ("django.contrib.auth.password_validation.CommonPasswordValidator"),
    },
    {
        "NAME": ("django.contrib.auth.password_validation.NumericPasswordValidator"),
    },
]

# 国際化設定
LANGUAGE_CODE = "ja"

# タイムゾーン設定
TIME_ZONE = "Asia/Tokyo"

# 国際化を有効化
USE_I18N = True

# タイムゾーンを有効化
USE_TZ = True

# 静的ファイルの URL
STATIC_URL = "static/"

# デフォルトの主キーフィールドタイプ
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Django REST Framework 設定
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 100,
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
    ],
}

# drf-spectacular（API ドキュメント生成）設定
SPECTACULAR_SETTINGS = {
    "TITLE": "TODO API",
    "DESCRIPTION": "Sample TODO API for testing article",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

# CORS 設定（開発用：全てのオリジンを許可）
# 本番環境では適切に制限する必要があります
CORS_ALLOW_ALL_ORIGINS = True
