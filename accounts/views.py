from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from .models import UserModel

@csrf_exempt
# Create your views here.
def sign_up_view(request):
    if request.method == 'GET':
        return HttpResponse('회원가입 창')
    elif request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        email = request.POST.get('email', '')
        github_address = request.POST.get('github_address', '')
        profile_image = request.POST.get('profile_image', None)

        exist_user = get_user_model().objects.filter(username=username)

        if password != password2:
            return HttpResponse('패스워드가 일치하지 않습니다.')
        elif username == '' or password == '':
            return HttpResponse('유저네임과 패스워드는 필수 입력 항목입니다.')
        elif exist_user:
            return HttpResponse('이미 존재하는 사용자입니다.')
        else:
            UserModel.objects.create_user(username=username, password=password, email=email, github_address=github_address, profile_image=profile_image)
            return HttpResponse('회원가입 성공!')