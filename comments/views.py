from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from code_feed.models import CodeModel
from .models import CommentModel
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed


@login_required
def create_view(request, code_id):
    if request.method == "POST":
        code = get_object_or_404(CodeModel, id=code_id)
        content = request.POST.get("content")
        code.comments.create(content=content, author=request.user)
        return redirect(reverse("code_feed:detail", args=[code_id]))
    else:
        return HttpResponseNotAllowed(["POST"])


@login_required
def update_view(request, code_id, comment_id):
    if request.method == "GET":
        comment = get_object_or_404(CommentModel, id=comment_id)
        if comment.author == request.user:
            return render(
                request,
                "code_feed/comment_form.html",
                {"code_id": code_id, "comment": comment},
            )
        else:
            return redirect(reverse("code:detail", args=[code_id]))
    elif request.method == "POST":
        comment = get_object_or_404(CommentModel, id=comment_id)
        comment.content = request.POST.get("content")
        comment.save()
        # 업데이트된 댓글로 리다이렉트
        return redirect(
            reverse("code_feed:detail", args=[code_id]) + f"#comment_{comment_id}"
        )
    else:
        return HttpResponseNotAllowed(["GET", "POST"])


@login_required
def delete_view(request, code_id, comment_id):
    if request.method == "POST":
        comment = get_object_or_404(CommentModel, id=comment_id)
        if comment.author == request.user:
            comment.delete()
        return redirect(reverse("code_feed:detail", args=[code_id]))
    else:
        return HttpResponseNotAllowed(["POST"])
