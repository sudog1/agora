from django.urls import path
from . import views

urlpatterns = [
    path("update/<int:code_id>/", views.update_view, name="update"),
]
