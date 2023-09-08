from django.db import models
from accounts.models import UserModel


class ProblemModel(models.Model):
    number = models.IntegerField(default=0)
    level = models.IntegerField(default=0)
    title = models.CharField(max_length=128)

    # (problem) N:N (user) 하나의 문제를 여러 유저가 해결할 수도 있고, 한 유저가 여러 문제를 해결할 수도 있습니다.
    solved = models.ManyToManyField(UserModel, related_name="solved")


class CodeModel(models.Model):
    content = models.TextField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="code")
    problem = models.ForeignKey(
        ProblemModel, on_delete=models.CASCADE, related_name="code"
    )

    # (code) N:N (user) 한 명의 유저는 많은 코드에 좋아요를 누를 수 있고, 하나의 코드에 많은 유저가 좋아요를 누를 수 있습니다.
    likes = models.ManyToManyField(UserModel, related_name="likes", blank=True)

    # (code) N:N (user) 북마크는 좋아요와 동일합니다.
    bookmarks = models.ManyToManyField(UserModel, related_name="bookmarks")


class CommentModel(models.Model):
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    post = models.ForeignKey(CodeModel, on_delete=models.CASCADE)
    content = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
