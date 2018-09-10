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

        city_list = CityDict.objects.all()

        hot_org = CourseOrg.objects.order_by('click_nums')[:3]

        # 城市筛选
        city_id = request.GET.get('city', '')
        if city_id:
            org_list = CourseOrg.objects.filter(city_id=city_id)

        # 机构类别筛选
        category = request.GET.get('ct','')
        if category:
            org_list = CourseOrg.objects.filter(category=category)

        sort = request.GET.get('sort','')
        if sort:
            if sort == 'students':
                org_list = org_list.order_by('-students')
            elif sort == 'courses':
                org_list = org_list.order_by('click_nums')

        org_count = org_list.count()

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(org_list, 3, request=request)

        org = p.page(page)

        return render(request, 'org-list.html', {'org_list': org,
                                                 'city_list': city_list,
                                                 'org_count': org_count,
                                                 'city_id': city_id,
                                                 'category': category,
                                                 'hot_org':hot_org,
                                                 'sort':sort
                                                 })
