from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseNotAllowed
from code_feed.models import ProblemModel, CodeModel, CommentModel
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    if request.method == 'GET':
        feeds = CodeModel.objects.all()
        context = {
            'feeds' : feeds,
        }
        return render(request, 'code_feed/index.html', context)
    else:
        return HttpResponse("invalid request method.", status=405)


@login_required
@csrf_exempt
def create(request):
    if request.method == 'GET':
        return render(request, 'code_feed/create.html')
    elif request.method == 'POST':
        CodeModel.objects.create(
            # problem=request.POST['problem'],
            content=request.POST['content'], 
            description=request.POST['description'],
            author=request.user,
        )
        return redirect('/code_feed/')
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
        if request.user in code.likes:
            code.likes.remove(request.user, code_id)
            return redirect("/code_feed/")
        else:
            code.likes.add(request.user, code_id)
            return redirect("/code_feed/")
    else:
        return HttpResponse("invalid request method.", status=405)

def bookmark(request, code_id):
    if request.method == "POST":
        code = get_object_or_404(CodeModel, id=code_id)
        if request.user in code.bookmark:
            code.bookmarks.remove(request.user, code_id)
            return redirect("/code_feed/")
        else:
            code.bookmarks.add(request.user, code_id)
            return redirect("/code_feed/")
    else:
        return HttpResponse("invalid request method.", status=405)