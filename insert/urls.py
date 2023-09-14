from django.urls import path
from . import views

app_name = "insert"

urlpatterns = [
    path("problems/", views.insert_problems_view, name="problems"),
    path("members/", views.insert_members_view, name="members"),
    path("codes/", views.insert_codes_view, name="codes"),
]
