from django.shortcuts import render,redirect
from .models import Fcuser
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password,check_password # 비밀번호 암호화
# from django.contrib.auth.hashers import make_password 
from .forms import Loginform

# Create your views here.
def home(request):
    user_id = request.session.get('user')
    
    if user_id:
        fcuser = Fcuser.objects.get(pk=user_id)
        return HttpResponse(fcuser.username)

    return HttpResponse('Home')

def logout(request):
    if request.session.get('user'):
        del request.session['user']
        return redirect('/')
    return redirect('../login')

def login(request):
    if request.method=='POST':
        login = Loginform(request.POST)
        if login.is_valid():
            request.session['user'] = login.user_id
            return redirect('/')
    else:
        login = Loginform()
    return render(request,'login.html',{'login':login})


def register(request):
    if request.method=='GET':
        return render(request,'register.html')
    elif request.method=='POST':
        username = request.POST.get('username',None)
        useremail = request.POST.get('email',None)
        password = request.POST.get('password',None)
        re_password = request.POST.get('re-password',None)

        res_data = {}

        if not (username and useremail and password and re_password):
            res_data['error'] = '모든 값을 입력해야합니다.'
        elif password != re_password:
            res_data['error'] = '비밀번호가 다릅니다.'
        else:
            fcuser = Fcuser(
                username=username,
                useremail=useremail,
                password=make_password(password)
            )
            fcuser.save()
        return render(request,'register.html',res_data)
        
