from django.db import models
from accounts.models import UserModel


class ProblemModel(models.Model):
    number = models.IntegerField(default=0)
    level = models.IntegerField(default=0)
    title = models.CharField(max_length=128)
    link = models.TextField()
    # (problem) N:N (user)
    solved = models.ManyToManyField(
        UserModel, through="CodeModel", related_name="solved", blank=True
    )


class CodeModel(models.Model):
    content = models.TextField(null=False, blank=False)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name="codes"
    )
    problem = models.ForeignKey(
        ProblemModel, on_delete=models.CASCADE, related_name="codes"
    )
    # (code) N:N (user)
    likes = models.ManyToManyField(UserModel, related_name="likes", blank=True)
    # (code) N:N (user)
    bookmarks = models.ManyToManyField(UserModel, related_name="bookmarks", blank=True)
