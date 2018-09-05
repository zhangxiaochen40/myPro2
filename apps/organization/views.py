# _*_ coding:utf-8 _*_
from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import CourseOrg,CityDict


class OrgListView(View):
    """
    课程机构功能
    """
    def get(self, request):

        org_list = CourseOrg.objects.all()
        org_count= org_list.count()
        city_list = CityDict.objects.all()

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(org_list, 3, request=request)

        org = p.page(page)

        return render(request, 'org-list.html', {'org_list': org, 'city_list': city_list,'org_count': org_count})
