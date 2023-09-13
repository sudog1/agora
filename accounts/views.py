from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from .models import UserModel
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from code_feed.models import ProblemModel, CodeModel, CommentModel
from .forms import CustomUserCreationForm

@csrf_exempt
def sign_up_view(request):
    if request.method == 'GET':
        return render(request, 'accounts/signup.html')
    elif request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        email = request.POST.get('email', '')
        github_address = request.POST.get('github_address', '')
        profile_image = request.FILES.get('profile_image', None)

        exist_user = get_user_model().objects.filter(username=username)

        if password != password2:
            return render(request, 'accounts/signup.html', {'error': '패스워드가 일치하지 않습니다.'})
        elif username == '' or password == '':
            return render(request, 'accounts/signup.html', {'error': '유저네임과 패스워드는 필수 입력 항목입니다.'})
        elif exist_user:
            return render(request, 'accounts/signup.html', {'error': '이미 존재하는 사용자입니다.'})
        else:
            user = UserModel.objects.create_user(username=username, password=password, email=email, github_address=github_address, profile_image=profile_image)
            return HttpResponse('회원가입 성공!')

@csrf_exempt
def sign_up(request):
    if request.method == 'GET':
        form = CustomUserCreationForm()
        context = {
            'form' : form,
        }
        return render(request, 'accounts/signup.html', context)
    elif request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid() :
            user = form.save()
            return render(request, 'accounts/signin.html', {'notice': '회원가입 완료! 로그인을 해주세요.'})
        else:
            return render(request, 'accounts/signup.html', {'error': form.errors})
            

@csrf_exempt
def mypage_view(request):
    if request.method == 'GET':
        user = request.user
        feeds = CodeModel.objects.all()
        context = {
            "feeds": feeds,
        }
        return render(request, 'accounts/mypage.html', context)

@csrf_exempt
def sign_in_view(request):
    if request.method == 'POST': 
        username = request.POST.get('username',None) 
        password = request.POST.get('password',None) 

        me = auth.authenticate(request, username=username, password=password) #=> 암호화 된 비밀번호와 사용자가 적은 비밀번호와 일치하는지 비교
        if me is not None:
            auth.login(request, me)
            return redirect('/mypage/')
        else:
            return redirect('/sign-in')
    elif request.method == 'GET':
        return render(request, 'accounts/signin.html')


@login_required
def logout_view(request):
    auth.logout(request)
    return redirect('/sign-in/')