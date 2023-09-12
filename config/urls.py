from django.contrib import admin
from django.urls import path, include
from config import settings, views
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    
    # 루트 url 처리
    path("", views.home_view, name="home"),

    # accounts 네임스페이스
    path("accounts/", include("accounts.urls", namespace="accounts")),

    # code_feed 네임스페이스
    path("code_feed/", include("code_feed.urls", namespace="code_feed")),

    # 데이터 삽입을 위한 insert 네임스페이스
    path("insert/", include("insert.urls", namespace="insert")),
]

# 미디어 파일은 개발 중에만 이 방식으로 사용합니다.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
