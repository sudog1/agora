from django.db import models
from accounts.models import UserModel
from code_feed.models import CodeModel


# Create your models here.
class CommentModel(models.Model):
    author = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name="comments"
    )
    code = models.ForeignKey(
        CodeModel, on_delete=models.CASCADE, related_name="comments"
    )
    content = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
