from django.db import connection
from django.forms import ValidationError
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
from django.db.models import Count


def signup_view(request):
    if request.method == "GET":
        form = CustomUserCreationForm()
        context = {
            "form": form,
        }
        return render(request, "accounts/signup.html", context)
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user:
                auth.login(request, user)
                return redirect(LOGIN_REDIRECT_URL)
            else:
                form.add_error("username", "해당 사용자 이름은 이미 존재합니다.")
        context = {
            "form": form,
            "errors": form.errors,
        }
        return render(request, "accounts/signup.html", context)
    else:
        # 허용된 api method에 대해서만 응답하고 그렇지 않은 경우 405에러를 발생시킵니다.
        return HttpResponseNotAllowed(["GET", "POST"])


@login_required
def mypage_view(request, user_id):
    if request.method == "GET":
        page_user = UserModel.objects.get(id=user_id)
        user = request.user
        feeds = (
            CodeModel.objects.select_related("author", "problem")
            .filter(author=page_user)
            .annotate(Count("likes"))
            .order_by("-created_at")
        )
        cur_page = max(int(request.GET.get("page", "1")), 1)

        page_obj, page_range = paginate(feeds, cur_page)
        bookmarked_codes = page_user.bookmarks.annotate(Count("likes")).order_by(
            "-created_at"
        )
        context = {
            "user": user,
            "page_user": page_user,
            "feeds": page_obj,
            "page_range": page_range,
            "bookmarked_codes": bookmarked_codes,
        }
        return render(request, "accounts/mypage.html", context)
    elif request.method == "POST":
        user = request.user
        page_user = UserModel.objects.get(id=user_id)
        feeds = CodeModel.objects.all()

        email = request.POST.get("email")
        github_address = request.POST.get("github_address")
        profile_image = request.FILES.get("profile_image", None)

        if profile_image == None:
            profile_image = user.profile_image
        if request.POST.get("profile_image_delete") == "True":
            profile_image = None

        print(request.POST)

        user.email = email
        user.github_address = github_address
        user.profile_image = profile_image
        user.save()

        context = {
            "user": user,
            "page_user": page_user,
            "feeds": feeds,
        }
        return redirect(f"/accounts/mypage/{user_id}")
    else:
        # 허용된 api method에 대해서만 응답하고 그렇지 않은 경우 405에러를 발생시킵니다.
        return HttpResponseNotAllowed(["GET", "POST"])


def login_view(request):
    if request.method == "GET":
        return render(request, "accounts/login.html")
    elif request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        auth_user = auth.authenticate(request, username=username, password=password)
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
        members = (
            UserModel.objects.filter(track=request.user.track)
            .values(
                "id",
                "username",
                "score",
            )
            .order_by("-username")
        )
        top_rankers = UserModel.objects.filter(track=request.user.track).order_by(
            "-score"
        )[:10]
        return render(
            request,
            "accounts/members.html",
            {"members": members, "top_rankers": top_rankers},
        )
