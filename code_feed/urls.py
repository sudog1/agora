from django.urls import path
from . import views

app_name = "code_feed"

urlpatterns = [
    path("", views.index),
    path("create/", views.create, name="create"),
    path("update/<int:code_id>/", views.update_view, name="update"),
    path("problems/", views.problems_view, name="problems"),
    path("insert/problems/", views.insert_problems_view, name="insert")
]
