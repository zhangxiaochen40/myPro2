# _*_ encoding:utf-8 _*_
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.views.generic import View
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
import json

from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm, ForgetPwdForm, ModifyPwdForm, UploadImageForm, UserInfoForm
from utlis.email_send import send_register_email
from organization.models import CourseOrg, Teacher
from courses.models import Course
from .models import Banner
from operation.models import UserCourse, UserFavorite


class CustomBackend(ModelBackend):
    """用户名验证"""

    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LoginView(View):
    """用户登陆"""

    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse("index"))
                else:
                    return render(request, "login.html", {"msg": "用户未激活！"})
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误！"})
        else:
            return render(request, "login.html", {"login_form": login_form})


class ForgetView(View):
    """忘记密码"""

    def get(self, request):
        forget_form = ForgetPwdForm()
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetPwdForm(request.POST)
        if forget_form.is_valid():
            email = forget_form.email
            send_register_email(email, 'forget')
            return render(request, 'send_success.html', {'forget_form', forget_form})


class ActiveView(View):
    """密码激活"""

    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
            return render(request, 'login.html')
        else:
            return render(request, 'active_fail.html')


class ResetPwdView(View):
    """重置密码"""

    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, 'password_reset.html', {'email': email})
        else:
            return render(request, 'active_fail.html')

        return render(request, 'login.html')


class ModifyPwdView(View):
    """重置密码"""

    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {'msg': '密码不一致'})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd1)
            user.save()
            return render(request, 'login.html')
        else:
            email = request.POST.get('email', '')
            return render(request, 'password_reset.html', {'modify_form': modify_form, 'email': email})


class RegisterView(View):
    """注册"""
    """注册"""

    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = request.POST.get('email', '')
            password = request.POST.get('password', '')
            if UserProfile.objects.filter(email=username):
                return render(request, 'register.html', {'register_form': register_form, 'msg': '用户已经存在'})

            user_profile = UserProfile()
            user_profile.username = username
            user_profile.email = username
            pwd = make_password(password)
            user_profile.password = pwd
            user_profile.is_active = False
            user_profile.save()

            send_register_email(username, 'register')
            return render(request, 'login.html')
        else:
            return render(request, 'register.html', '{}')


class IndexView(View):
    # real在线网 首页
    def get(self, request):
        # 取出轮播图
        all_banners = Banner.objects.all().order_by('index')
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request, 'index.html', {
            'all_banners': all_banners,
            'courses': courses,
            'banner_courses': banner_courses,
            'course_orgs': course_orgs
        })


class UserInfoView(View):
    """
    用户信息界面
    """
    def get(self, request):
        return render(request, 'usercenter-info.html',{

        })

    def post(self,request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse("{'status':'success'}", content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


class UploadImageView(View):
    """
    修改用户头像
    """
    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse("{'status':'success'}", content_type='application/json')
        return HttpResponse("{'status':'fail'}", content_type='application/json')


class UpdatePwdView(View):
    """在用户中心修改用户密码"""
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            if pwd1 != pwd2:
                return HttpResponse("{'status':'fail', 'msg':'密码不一致'}", content_type='application/json')
            user = request.user
            user.password = make_password(pwd1)
            user.save()
            return HttpResponse("{'status': 'success'}", content_type='application/json')
        else:
            return HttpResponse("{'status':'fail', 'msg':'输入错误'}", content_type='application/json')


class SendEmailCodeView(View):
    """发送邮箱验证码"""
    def get(self,request):
        email = request.POST.get('email', '')
        if UserProfile.objects.filter(email=email):
            return HttpResponse("{'email', '邮箱已经存在'}", content_type='application/json')
        send_register_email(email, 'update_email')
        return HttpResponse('{"status":"success"}', content_type='application/json')


class UpdateEmailView(View):
    """修改邮箱"""
    def post(self,request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')
        if EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update_email'):
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse("{'email':'验证码错误'}", content_type='application/json')


class MyCoursesView(View):
    """我的课程"""
    def get(self, request):
        my_course = UserCourse.objects.filter(user=request.user)
        return render(request, 'usercenter-mycourse.html', {
            'my_course': my_course
        })


class MyfavOrgView(View):
    """我收藏的课程机构"""
    def get(self, request):
        org_list = []
        favs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav in favs:
            org = CourseOrg.objects.get(id=fav.fav_id)
            org_list.append(org)
        return render(request,'usercenter-fav-org.html',{
            'org_list': org_list
        })


class MyFavCourseView(View):
    """我的课程收藏"""
    def get(self, request):
        course_list = []
        user_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        if user_courses:
            for user_course in user_courses:
                course = Course.objects.filter(id=user_course.fav_id)
                course_list.append(course)
        return render(request, 'usercenter-fav-course.html', {
            'course_list': course_list
        })


class MyFavTeacherView(View):
    """
    我的教师收藏
    """
    def get(self, request):
        treacher_list = []
        teacher_ids = UserFavorite.objects.filter(user=request.user, fav_type=3)
        if teacher_ids:
            for teacher_id in teacher_ids:
                teacher = Teacher.objects.get(id=teacher_id)
                treacher_list.append(teacher)
        return render(request, 'usercenter-fav-teacher.html', {
            'treacher_list': treacher_list
        })
