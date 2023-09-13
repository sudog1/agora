from django.http import HttpResponseNotAllowed
from django.shortcuts import redirect, render
from django.urls import reverse
from accounts.models import UserModel
from code_feed.models import ProblemModel
from django.contrib.auth.decorators import login_required
import csv


@login_required
def insert_members_view(request):
    if request.method == "GET":
        csv_file_path = "users.csv"
        with open(csv_file_path, "r", encoding="utf-8") as csv_file:
            csv_rows = csv.reader(csv_file)
            next(csv_rows)
            for row in csv_rows:
                name = row[0]
                if UserModel.objects.filter(username=name).exists():
                    break
                UserModel.objects.create_user(
                    username=name,
                    password="1234",
                    email="",
                    github_address="",
                )
        return redirect(reverse("accounts:members"))
    else:
        return HttpResponseNotAllowed(["GET"])


@login_required
def insert_problems_view(request):
    if request.method == "GET":
        csv_file_path = "problems.csv"
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


@login_required
def insert_codes_view(request):
    if request.method == "GET":
        csv_file_path = "codes.csv"
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
