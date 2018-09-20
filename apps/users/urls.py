# _*_ coding: utf-8 _*_
from django.conf.urls import url, include

from .views import UserInfoView, UploadImageView, UpdatePwdView, SendEmailCodeView, UpdateEmailView, MyCoursesView
from .views import MyfavOrgView, MyFavCourseView, MyFavTeacherView

urlpatterns = [
    # 用户信息
    url(r'^info/', UserInfoView.as_view(), name='user_info'),
    # 修改用户头像
    url(r'^image/upload/$', UploadImageView.as_view(), name='image_upload'),
    # 修该用户密码
    url(r'^update/pwd/$', UpdatePwdView.as_view(), name="update_pwd"),
    # 发送邮箱验证码
    url(r'^sendemail_code/', SendEmailCodeView.as_view(), name='sendemail_code'),
    # 修改邮箱
    url(r'^update_email', UpdateEmailView.as_view(), name='update_email'),
    # 我的课程
    url(r'^mycourse/', MyCoursesView.as_view(), name='mycourse'),
    # 课程机构收藏
    url(r'^myfav_org', MyfavOrgView.as_view(), name='myfav_org'),
    # 课程收藏
    url(r'^myfav_course', MyFavCourseView.as_view(), name='myfav_course'),
    # 收藏讲师
    url(r'^myfav_teacher', MyFavTeacherView.as_view(), name='myfav_teacher')

]