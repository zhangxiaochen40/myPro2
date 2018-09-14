# _*_coding:utf-8 _*_

from django.conf.urls import url, include
from .views import OrgListView, AddAskView, OrgHomeView, OrgCourseView, OrgDescView, OrgTeacherView, AddFavView, TeacherListView

urlpatterns = [
    # 课程机构列表页
    url(r'^list/', OrgListView.as_view(), name='org_list'),
    url(r'^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name='org_home'),
    url(r'^course/(?P<org_id>\d+)/$', OrgCourseView.as_view(), name='org_course'),
    url(r'^desc/(?P<org_id>\d+)/$', OrgDescView.as_view(), name='org_desc'),
    url(r'^teacher/(?P<org_id>\d+)', OrgTeacherView.as_view(), name='org_teacher'),
    # 用户咨询
    url(r'^add_ask', AddAskView.as_view(), name='add_ask'),

    # 教师列表
    url(r'^teacher/list/$', TeacherListView.as_view(), name='teacher_list'),
    # 用户收藏或者取消收藏
    url(r'^add_fav', AddFavView.as_view(), name='add_fav'),


]
