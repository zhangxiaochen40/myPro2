# _*_ coding: utf-8 _*_
from django.conf.urls import url, include

from .views import UserInfoView, UploadImageView

urlpatterns = [
    # 用户信息
    url(r'^info/', UserInfoView.as_view(), name='user_info'),
    # 修改用户头像
    url(r'^image/upload/$', UploadImageView.as_view(), name='image_upload')
]