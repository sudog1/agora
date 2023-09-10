from django.shortcuts import render, redirect
from django.http import HttpResponse
from code_feed.models import ProblemModel, CodeModel, CommentModel
from django.views.decorators.csrf import csrf_exempt
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


# @login_required(login_url="/user/login/")
# @csrf_exempt
def create(request):
    if request.method == 'GET':
        return render(request, 'code_feed/create.html')
    elif request.method == 'POST':
        CodeModel.objects.create(
            problem=request.POST['problem'],
            content=request.POST['content'], 
            description=request.POST['description'],
            author=request.author,
        )
        return redirect('/code_feed/')
    else:
        return HttpResponse("invalid request method.", status=405)