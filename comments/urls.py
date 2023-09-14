from django.urls import path
from . import views

app_name = "comments"

urlpatterns = [
    path("create/", views.create_view, name="create"),
    path("update/<int:comment_id>/", views.update_view, name="update"),
    path("delete/<int:comment_id>/", views.delete_view, name="delete"),
]
