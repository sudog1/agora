from django.urls import path
from . import views

app_name = "insert"

urlpatterns = [
    path("problems/", views.insert_problems_view, name="problems"),
    # path("codes/", views.insert_codes_view, name="codes"),
]