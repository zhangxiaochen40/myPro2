# _*_ encoding:utf-8 _*_
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.views.generic import View
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth.hashers import make_password

from .models import UserProfile,EmailVerifyRecord
from .forms import LoginForm,RegisterForm,ForgetPwdForm
from utlis.email_send import send_register_email


class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LoginView(View):

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return request(request, 'index.html', {})
                else:
                    return render(request, 'login.html', {'msg': '用户名未激活！'})
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误！'})
        else:
            return render(request, "login.html", {"login_form": login_form})

    def get(self, request):

        return render(request, 'login.html', {})


class ForgetView(View):
    def get(self,request):
        forget_form=ForgetPwdForm()
        return render(request,'forgetpwd.html',{'forget_form':forget_form})

    def post(self,request):
        forget_form=ForgetPwdForm(request.POST)
        if forget_form.is_valid():
            email=forget_form.email
            send_register_email(email,'forget')
            return render(request,'send_success.html',{'forget_form',forget_form})


class ActiveView(View):
    def get(self,request,active_code):
        all_records=EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email=record.email
                user=UserProfile.objects.get(email=email)
                user.is_active=True
            return render(request,'login.html')
        else:
            return render(request,'active_fail.html')

class RegisterView(View):
    def get(self,request):
        register_form = RegisterForm()
        return render(request,'register.html',{'register_form':register_form})

    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = request.POST.get('email', '')
            password = request.POST.get('password', '')
            if UserProfile.objects.filter(email=username):
                return render(request, 'register.html', {'register_form': register_form,'msg':'用户已经存在'})

            user_profile=UserProfile()
            user_profile.username=username
            user_profile.email=username
            pwd= make_password(password)
            user_profile.password=pwd
            user_profile.is_active=False
            user_profile.save()

            send_register_email(username,'register')
            return render(request,'login.html')
        else:
            return render(request,'register.html','{}')
