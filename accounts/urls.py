from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('sign-up/', views.sign_up, name='sign-up'),
    path('mypage/', views.mypage_view, name='mypage'),
    path('sign-in/', views.sign_in_view, name='sign-in' ),
    path('logout/', views.logout_view, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)