from django.urls import path
from . import views

app_name = "code_feed"

urlpatterns = [
    # 함수 이름들 <func_name>_view로 통일하겠습니다.
    path("", views.index_view, name="index"),
    path("detail/<int:code_id>/", views.detail_view, name="detail"),
    path("create_feed/", views.create_view, name="create"),
    path("update/<int:code_id>/", views.update_view, name="update"),
    path("delete/<int:code_id>/", views.delete_view, name="delete"),
    path("likes/<int:code_id>/", views.likes_view, name="likes"),
    path("bookmarks/<int:code_id>/", views.bookmarks_view, name="bookmarks"),
    path("problems/", views.problems_view, name="problems"),
    path("insert/problems/", views.insert_problems_view, name="insert")
]
