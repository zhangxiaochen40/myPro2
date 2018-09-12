# _*_ coding: utf-8 _*_
from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import Course

# Create your views here.


class CourseListView(View):
    """课程列表页"""
    def get(self, request):

        all_courses = Course.objects.all().order_by('-add_time')
        hot_courses = Course.objects.all().order_by('-click_nums')[:3]

        sort = request.GET.get('sort', '')
        if sort:
            # 按学习人数排序
            if sort == 'students':
                all_courses = all_courses.order_by('-students')
            # 按点击数排序
            if sort == 'hot':
                all_courses = all_courses.order_by('-click_nums')

        # 对课程列表进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, 3, request=request)

        courses = p.page(page)

        return render(request, 'course-list.html', {
            'all_courses': courses,
            'hot_courses': hot_courses,
            'sort': sort
        })