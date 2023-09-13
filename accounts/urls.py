from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    # 함수 이름들 <func_name>_view로 통일하겠습니다.
    # 통일을 위해 sign-up, sign-in을 각각 signup, login으로 변경하였습니다.
    path("signup/", views.sign_up, name="signup"),
    path("mypage/<int:user_id>", views.mypage_view, name="mypage"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]
