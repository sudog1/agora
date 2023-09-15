from django.http import HttpResponseNotAllowed
from django.shortcuts import redirect
from django.urls import reverse
from accounts.models import UserModel
from code_feed.models import CodeModel, ProblemModel
from django.contrib.auth.decorators import login_required
import csv
from datetime import datetime


# @login_required
def insert_members_view(request):
    if request.method == "GET":
        csv_file_path = "members.csv"
        with open(csv_file_path, "r", encoding="utf-8") as csv_file:
            csv_rows = csv.reader(csv_file)
            next(csv_rows)
            for name, track in csv_rows:
                if UserModel.objects.filter(username=name).exists():
                    break
                UserModel.objects.create_user(
                    username=f"{name}_{track}",
                    password="1234",
                    track=track,
                    email="",
                    github_address="",
                )
        return redirect(reverse("accounts:members"))
    else:
        return HttpResponseNotAllowed(["GET"])


# @login_required
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


# @login_required
def insert_codes_view(request):
    if request.method == "GET":
        csv_file_path = "codes.csv"
        with open(csv_file_path, "r", encoding="utf-8") as csv_file:
            date_format = "%Y. %m. %d %p %I:%M:%S"
            csv_rows = csv.DictReader(csv_file)
            for row in csv_rows:
                timestamp = row["timestamp"]
                date_string = timestamp.replace("오후", "PM").replace("오전", "AM")
                date_object = datetime.strptime(date_string, date_format)
                created_at = date_object.strftime("%Y-%m-%d %H:%M:%S")
                name = row["name"]
                track = row["track"]
                if not UserModel.objects.filter(username=f"{name}_{track}").exists():
                    continue
                author = UserModel.objects.get(username=f"{name}_{track}")
                code_content = row["code"]
                problem_number = row["problem_number"]
                problem = ProblemModel.objects.get(number=problem_number)
                level = row["level"]
                author.score += int(level)
                author.save()
                CodeModel.objects.create(
                    content=code_content,
                    author=author,
                    problem=problem,
                    created_at=created_at,
                )
        return redirect(reverse("code_feed:problems"))
    else:
        return HttpResponseNotAllowed(["GET"])
