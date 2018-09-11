# _*_coding:utf-8 _*_

from django.conf.urls import url, include
from .views import OrgListView, AddAskView, OrgHomeView, OrgCourseView, OrgDescView

urlpatterns = [
    # 课程机构列表页
    url(r'^list/', OrgListView.as_view(), name='org_list'),
    url(r'^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name='org_home'),
    url(r'^course/(?P<org_id>\d+)/$', OrgCourseView.as_view(), name='org_course'),
     url(r'^desc/(?P<org_id>\d+)/$',OrgDescView.as_view(), name='org_desc'),
    # 用户咨询
    url(r'^add_ask', AddAskView.as_view(), name='add_ask'),


]
