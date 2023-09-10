from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from code_feed.models import CodeModel, ProblemModel


@login_required
def update_view(request, code_id):
    if request.method == "GET":
        code = get_object_or_404(CodeModel, id=code_id)
        if code.author == request.user:
            return render(request, "code/form.html", {"code": code})
        else:
            return redirect(reverse("code_feed:detail", args=[code_id]))
    elif request.method == "POST":
        code = get_object_or_404(CodeModel, id=code_id)
        problem_id = request.POST.get("problem_id")
        problem = get_object_or_404(ProblemModel, id=problem_id)
        if code.problem != problem:
            code.author.score += problem.level - code.problem.level
            code.author.save()
            code.problem = problem
        code.content = request.POST.get("content")
        code.description = request.POST.get("description")
        code.save()
        return redirect(reverse("code_feed:detail", args=[code_id]))
    else:
        return HttpResponseNotAllowed(["GET", "POST"])
