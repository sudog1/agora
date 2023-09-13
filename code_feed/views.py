from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseNotAllowed
from code_feed.models import ProblemModel, CodeModel, CommentModel
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Count
import csv

# Create your views here.


def index(request):
    if request.method == "GET":
        feeds = CodeModel.objects.annotate(total_likes=Count('likes')).all()
        print(f"CodeModel.objects.annotate(total_likes=Count('likes')) : {type(CodeModel.objects.annotate(total_likes=Count('likes')).all())}")
        context = {
            "feeds": feeds,
        }
        return render(request, "code_feed/index.html", context)
    else:
        return HttpResponse("invalid request method.", status=405)


@login_required
def create(request):
    if request.method == "GET":
        return render(request, "code_feed/create.html")
    elif request.method == "POST":
        CodeModel.objects.create(
            # problem=request.POST['problem'],
            content=request.POST["content"],
            description=request.POST["description"],
            author=request.user,
        )
        return redirect("/code_feed/")
    else:
        return HttpResponse("invalid request method.", status=405)


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
        # problem_id = request.POST.get("problem_id")
        # problem = get_object_or_404(ProblemModel, id=problem_id)
        # if code.problem != problem:
        #     code.author.score += problem.level - code.problem.level
        #     code.author.save()
        #     code.problem = problem
        code.content = request.POST.get("content")
        code.description = request.POST.get("description")
        code.save()
        return redirect("/code_feed/")
    else:
        return HttpResponseNotAllowed(["GET", "POST"])

@csrf_exempt
def delete(request, code_id):
    if request.method == "POST":
        code = get_object_or_404(CodeModel, id=code_id)
        if request.user == code.user:
            code.delete()
            return redirect("/code_feed/")
        else:
            return HttpResponse("You are not allowed to delete this content.", status=403)
    else:
        return HttpResponse("invalid request method.", status=405)


def press_like(request, code_id):
    if request.method == "POST":
        code = get_object_or_404(CodeModel, id=code_id)
        print(f'\ntype(request.user):{type(request.user)}\n')
        print(f'\ntype(code.likes.all()):{type(code.likes.all())}\n')
        if request.user in code.likes:
            code.likes.remove(request.user)
        else:
            code.likes.add(request.user)
        return redirect("/code_feed/")
    else:
        return HttpResponse("invalid request method.", status=405)

def bookmark(request, code_id):
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

def insert_problems_view(request):
    if request.method == "GET":
        csv_file_path = "problem_list.csv"
        with open(csv_file_path, "r", encoding="utf-8") as csv_file:
            csv_rows = csv.reader(csv_file)
            next(csv_rows)
            for number, title, link, level in csv_rows:
                if ProblemModel.objects.filter(number=number).exists():
                    break
                ProblemModel.objects.create(
                    number=int(number),
                    title=title,
                    link=link,
                    level=int(level),
                )
        return redirect(reverse("code_feed:problems"))
    else:
        return HttpResponseNotAllowed(["GET"])


# @login_required
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