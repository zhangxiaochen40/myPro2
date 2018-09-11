# _*_ coding:utf-8 _*_
from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse

from .models import CourseOrg, CityDict
from .forms import UserAskForm


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
                                                 'hot_org': hot_org,
                                                 'sort': sort
                                                 })


class AddAskView(View):
    """
    用户咨询
    """
    def post(self, request):
        add_ask = UserAskForm(request.POST)
        if add_ask.is_valid():
            user_ask = add_ask.save(commit=True)
            return HttpResponse("{'status':'success'}", content_type='application/json')
        else:
            return HttpResponse("{'status':'fail','msg':'添加出错'}", content_type='application/json')


class OrgHomeView(View):
    """
    课程机构首页
    """
    def get(self, request, org_id):
        current_page = 'home'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_course = course_org.course_set().all()
        all_teacher = course_org.teacher_set.all()

        return render(request, 'org-detail-homepage.html', {
            'all_course': all_course,
            'all_teacher': all_teacher,
            'current_page': current_page,
            'course_org': course_org,
        })


class OrgCourseView(View):
    """
    机构课程列表
    """
    def get(self, request, org_id):
        current_page = 'course'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_course = course_org.course_set().all()

        return render(request, 'org-detail-course.html', {
            'all_course': all_course,
            'current_page': current_page,
            'course_org': course_org,
        })


class OrgDescView(View):
    """
    机构详情页
    """

    def get(self, request, org_id):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id=int(org_id))

        return render(request, 'org-detail-desc.html', {
            'current_page': current_page,
            'course_org': course_org,
        })




