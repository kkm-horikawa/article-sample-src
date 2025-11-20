"""プロジェクトのルート URL 設定モジュール。

TODO アプリケーションの URL パターンを定義します。

提供されるエンドポイント:
    - /admin/: Django 管理サイト
    - /api/: TODO API エンドポイント（api.urls に委譲）
    - /api/schema/: OpenAPI スキーマ（JSON 形式）
    - /api/docs/: Swagger UI による API ドキュメント
"""

from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]
