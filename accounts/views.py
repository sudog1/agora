from django.shortcuts import render, redirect
from django.http import HttpResponseNotAllowed
from django.contrib.auth import get_user_model
from code_feed.views import paginate
from config.settings import LOGIN_REDIRECT_URL, LOGOUT_REDIRECT_URL
from django.conf.global_settings import LOGIN_URL
from .models import UserModel
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from code_feed.models import ProblemModel, CodeModel
from .forms import CustomUserCreationForm


# sign-up 에서 signup으로 변경했습니다.
def signup_view(request):
    if request.method == "GET":
        return render(request, "accounts/signup.html")
    elif request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        password2 = request.POST.get("password2", "")
        email = request.POST.get("email", "")
        github_address = request.POST.get("github_address", "")
        profile_image = request.FILES.get("profile_image", None)
        exist_user = get_user_model().objects.filter(username=username)

        if password != password2:
            return render(
                request, "accounts/signup.html", {"error": "패스워드가 일치하지 않습니다."}
            )
        elif username == "" or password == "":
            return render(
                request, "accounts/signup.html", {"error": "유저네임과 패스워드는 필수 입력 항목입니다."}
            )
        elif exist_user:
            return render(request, "accounts/signup.html", {"error": "이미 존재하는 사용자입니다."})
        else:
            user = UserModel.objects.create_user(
                username=username,
                password=password,
                email=email,
                github_address=github_address,
                profile_image=profile_image,
            )
            auth.login(request, user)
            return redirect(LOGIN_REDIRECT_URL)
    else:
        # 허용된 api method에 대해서만 응답하고 그렇지 않은 경우 405에러를 발생시킵니다.
        return HttpResponseNotAllowed(["GET", "POST"])


def sign_up(request):
    if request.method == "GET":
        form = CustomUserCreationForm()
        context = {
            "form": form,
        }
        return render(request, "accounts/signup.html", context)
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            return redirect(LOGIN_REDIRECT_URL)
        else:
            return render(request, "accounts/signup.html", {"error": form.errors})


@login_required
def mypage_view(request, user_id):
    if request.method == "GET":
        page_user = UserModel.objects.get(id=user_id)
        user = request.user
        feeds = CodeModel.objects.all()
        cur_page = 1
        
        context = {
            "feeds": paginate(feeds, cur_page),
        }
        return render(request, "accounts/mypage.html", context)


# sign-in에서 login으로 변경했습니다.
def login_view(request):
    if request.method == "GET":
        return render(request, "accounts/login.html")
    elif request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        auth_user = auth.authenticate(
            request, username=username, password=password
        )  # => 암호화 된 비밀번호와 사용자가 적은 비밀번호와 일치하는지 비교
        if auth_user:
            auth.login(request, auth_user)
            return redirect(LOGIN_REDIRECT_URL)
        else:
            return redirect(LOGIN_URL)
    else:
        return HttpResponseNotAllowed(["GET", "POST"])


@login_required
def logout_view(request):
    if request.method == "POST":
        auth.logout(request)
        return redirect(LOGOUT_REDIRECT_URL)
    else:
        return HttpResponseNotAllowed(["POST"])


def members_view(request):
    if request.method == "GET":
        members = UserModel.objects.values("username", "score")
        return render(request, "accounts/members.html", {"members": members})
