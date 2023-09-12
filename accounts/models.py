from django.db import models
from django.contrib.auth.models import AbstractUser


class UserModel(AbstractUser):
    score = models.IntegerField(default=0)
    github_address = models.CharField(max_length=64, blank=True)
    profile_image = models.ImageField(upload_to="", blank=True)
