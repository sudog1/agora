from django.urls import path
from . import views

app_name = "code_feed"

urlpatterns = [
    path("update/<int:code_id>/", views.update_view, name="update"),
]
