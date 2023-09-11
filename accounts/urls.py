from django.urls import path
from . import views

urlpatterns = [
    path('sign-up/', views.sign_up_view, name='sign-up'),
    path('mypage/', views.mypage_view, name='mypage'),
    path('sign-in/', views.sign_in_view, name='sign-in' ),
]