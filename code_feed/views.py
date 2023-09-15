from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseNotAllowed
from code_feed.models import ProblemModel, CodeModel
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.core.paginator import Paginator
from config.settings import PAGE_RANGE, PER_PAGE
from django.db import connection
from accounts.models import UserModel


def paginate(feeds, cur_page):
    paginator = Paginator(feeds, PER_PAGE)
    page_obj = paginator.get_page(cur_page)
    if PAGE_RANGE * 2 > paginator.num_pages:
        page_head = 1
        page_tail = paginator.num_pages + 1
    else:
        page_head = cur_page - PAGE_RANGE
        page_tail = cur_page + PAGE_RANGE
        if page_head < 1:
            page_tail += 1 - page_head
            page_head = 1
        elif page_tail > paginator.num_pages:
            page_head -= page_tail - paginator.num_pages - 1
            page_tail = paginator.num_pages + 1
    return [page_obj, range(page_head, page_tail)]


@login_required
def index_view(request):
    if request.method == "GET":
        user = request.user
        feeds = (
            CodeModel.objects.filter(author__track=user.track)
            .select_related("author", "problem")
            .annotate(Count("likes"))
            .order_by("-created_at")
        )
        # a = len(connection.queries)
        # print(f"실행된 쿼리 수: {a}")
        # for feed in feeds:
        #     print(feed.author.username)
        # a = len(connection.queries)
        # print(f"실행된 쿼리 수: {a}")
        cur_page = max(int(request.GET.get("page", "1")), 1)
        page_obj, page_range = paginate(feeds, cur_page)

        top_rankers = UserModel.objects.filter(track=user.track).order_by("-score")[:10]
        if user.track == "AI":
            lang = "python"
        else:
            lang = "java"
        context = {
            "feeds": page_obj,
            "page_range": page_range,
            "top_rankers": top_rankers,
            "lang": lang,
        }
        return render(request, "code_feed/index.html", context)
    else:
        return HttpResponseNotAllowed(["GET"])


@login_required
def detail_view(request, code_id):
    code = CodeModel.objects.get(id=code_id)
    comments = code.comments.order_by("-created_at")
    context = {
        "code": code,
        "comments": comments,
    }
    return render(request, "code_feed/detail.html", context)


@login_required
def create_view(request, problem_id):
    if request.method == "GET":
        problem = get_object_or_404(ProblemModel, number=problem_id)
        code = CodeModel.objects.filter(problem=problem_id, author=request.user.id)
        context = {
            "problem": problem,
        }
        if code.exists():
            context["code"] = code[0]
        return render(request, "code_feed/create.html", context)
    elif request.method == "POST":
        problem = get_object_or_404(ProblemModel, number=problem_id)
        user = request.user
        user.score += problem.level
        user.save()
        CodeModel.objects.create(
            problem=problem,
            content=request.POST.get("content"),
            description=request.POST.get("description"),
            author=user,
        )
        return redirect(reverse("code_feed:index"))
    else:
        return HttpResponseNotAllowed(["GET", "POST"])


@login_required
def update_view(request, code_id):
    if request.method == "GET":
        code = get_object_or_404(CodeModel, id=code_id)
        problem = code.problem
        if code.author == request.user:
            return render(
                request, "code_feed/create.html", {"code": code, "problem": problem}
            )
        else:
            return redirect(reverse("code_feed:detail", args=[code_id]))
    elif request.method == "POST":
        code = get_object_or_404(CodeModel, id=code_id)

        code.content = request.POST.get("content")
        code.description = request.POST.get("description")
        code.save()
        return redirect(reverse("code_feed:detail", args=[code_id]))
    else:
        return HttpResponseNotAllowed(["GET", "POST"])


@login_required
def delete_view(request, code_id):
    if request.method == "POST":
        code = get_object_or_404(CodeModel, id=code_id)
        if request.user == code.user:
            code.delete()
            return redirect(reverse("code_feed:index"))
        else:
            return HttpResponse(
                "You are not allowed to delete this content.", status=403
            )
    else:
        return HttpResponseNotAllowed(["POST"])


@login_required
def likes_view(request, code_id):
    if request.method == "POST":
        code = get_object_or_404(CodeModel, id=code_id)
        if request.user != code.author:
            if request.user in code.likes.all():
                code.likes.remove(request.user)
            else:
                code.likes.add(request.user)
            return redirect(reverse("code_feed:detail", args=[code_id]))
        else:
            return redirect(reverse("code_feed:detail", args=[code_id]))
    else:
        return HttpResponseNotAllowed(["POST"])


@login_required
def bookmarks_view(request, code_id):
    if request.method == "POST":
        code = get_object_or_404(CodeModel, id=code_id)
        if request.user != code.author:
            if request.user in code.bookmarks.all():
                code.bookmarks.remove(request.user)
            else:
                code.bookmarks.add(request.user)
            return redirect(reverse("code_feed:detail", args=[code_id]))
        else:
            return redirect(reverse("code_feed:detail", args=[code_id]))
    else:
        return redirect(reverse("code_feed:detail", args=[code_id]))


def problems_view(request):
    if request.method == "GET":
        problems = ProblemModel.objects.values_list("number", "title", "link", "level")
        top_rankers = UserModel.objects.filter(track=request.user.track).order_by(
            "-score"
        )[:10]
        color_types = [
            "",
            "table-default",
            "table-primary",
            "table-success",
            "table-warning",
            "table-danger",
        ]
        problems = map(lambda x: (x[0], x[1], x[2], x[3], color_types[x[3]]), problems)
        return render(
            request,
            "code_feed/problems.html",
            {"problems": problems, "top_rankers": top_rankers},
        )
    else:
        return HttpResponseNotAllowed(["GET"])
