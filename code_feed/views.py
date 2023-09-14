from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseNotAllowed
from code_feed.models import ProblemModel, CodeModel
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.core.paginator import Paginator
from config.settings import PAGE_RANGE, PER_PAGE
from django.db import connection


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
    return {"feeds": page_obj, "page_range": range(page_head, page_tail)}


def index_view(request):
    if request.method == "GET":
        # track = request.GET.get("track")
        feeds = (
            CodeModel.objects.filter(author__track="AI")
            .select_related("author", "problem")
            .annotate(Count("likes"))
            .order_by("-created_at")
        )
        a = len(connection.queries)

        # 쿼리가 실제로 몇번 수행되는지 확인할 수 있습니다.
        print(f"실행된 쿼리 수: {a}")
        for feed in feeds:
            print(feed.author)
            print(feed.problem.title)
        b = len(connection.queries)
        print(f"실행된 쿼리 수: {b}")

        cur_page = max(int(request.GET.get("page", "1")), 1)
        context = paginate(feeds, cur_page)
        # if track == "AI":
        #     context["lang"] = "python"
        # else:
        #     context["lang"] = "java"
        return render(request, "code_feed/index.html", context)
    else:
        return HttpResponseNotAllowed(["GET"])


@login_required
def detail_view(request, code_id):
    pass


@login_required
def create_view(request):
    if request.method == "GET":
        return render(request, "code_feed/create.html")
    elif request.method == "POST":
        problem = get_object_or_404(ProblemModel, number=request.POST("problem_num"))
        user = request.user
        user.score += problem.level
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
        if code.author == request.user:
            return render(request, "code_feed/create.html", {"code": code})
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
        return HttpResponse("invalid request method.", status=405)


@login_required
def likes_view(request, code_id):
    if request.method == "POST":
        code = get_object_or_404(CodeModel, id=code_id)
        if request.user in code.likes.all():
            code.likes.remove(request.user)
        else:
            code.likes.add(request.user)
        return redirect("/code_feed/")
    else:
        return HttpResponse("invalid request method.", status=405)


@login_required
def bookmarks_view(request, code_id):
    if request.method == "POST":
        code = get_object_or_404(CodeModel, id=code_id)
        if request.user in code.bookmarks.all():
            code.bookmarks.remove(request.user)
            return redirect("/code_feed/")
        else:
            code.bookmarks.add(request.user)
            return redirect("/code_feed/")
    else:
        return HttpResponse("invalid request method.", status=405)


def problems_view(request):
    if request.method == "GET":
        problems = ProblemModel.objects.values_list("number", "title", "link", "level")
        color_types = [
            "",
            "table-default",
            "table-primary",
            "table-success",
            "table-warning",
            "table-danger",
        ]
        problems = map(lambda x: (x[0], x[1], x[2], x[3], color_types[x[3]]), problems)
        return render(request, "code_feed/problems.html", {"problems": problems})
    else:
        return HttpResponseNotAllowed(["GET"])
