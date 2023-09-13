from django.http import HttpResponseNotAllowed
from django.shortcuts import render


def home_view(request):
    if request.method == "GET":
        return render(request, "home.html")
    else:
        return HttpResponseNotAllowed(["GET"])
