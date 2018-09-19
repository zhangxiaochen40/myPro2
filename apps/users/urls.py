# _*_ coding: utf-8 _*_
from django.conf.urls import url, include

from .views import UserInfoView, UploadImageView, UpdatePwdView, SendEmailCodeView, UpdateEmailView, MyCoursesView

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
    url(r'^mycourse/', MyCoursesView.as_view(), name='mycourse')

]