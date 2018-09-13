# _*_ coding: utf-8 _*_
from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse

from .models import Course, CourseResource
from operation.models import UserFavorite, CourseComments

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


class CourseDetailView(View):
    """
    课程详情页
    """
    def get(self, request, course_id):

        course = Course.objects.get(id=int(course_id))
        # 点击数加一
        course.click_nums += 1
        course.save()

        fav_org = False
        fav_course = False
        # 判断是否收藏
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course_id), fav_type=2):
                fav_org = True
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course_id), fav_type=1):
                fav_course = True

        # 相关课程
        tag = course.tag
        if tag:
            relate_course = Course.objects.filter(tag=tag)[:1]
        else:
            relate_course = []
        return render(request, 'course-detail.html', {
            'course': course,
            'relate_course': relate_course,
            'fav_course': fav_course,
            'fav_org': fav_org
        })


class CourseInfoView(View):
    """
    课程详情
    """
    def get(self, request, course_id):

        course_info = Course.objects.get(id=int(course_id))
        lessons = course_info.get_lesson(request)
        # 课程资源
        all_resources = CourseResource.objects.filter(course=course_info)

        return render(request, 'course-video.html', {
            'course_info': course_info,
            'all_resources': all_resources,
            'lessons': lessons
        })


class CourseCommentView(View):
    """
    课程评论
    """
    def get(self, request, course_id):

        course_info = Course.objects.get(id=int(course_id))
        lessons = course_info.get_lesson(request)
        # 课程资源
        all_resources = CourseResource.objects.filter(course=course_info)
        # 当前课程的所有评论
        all_comment = CourseComments.objects.filter(course=course_info)

        return render(request, 'course-comment.html', {
            'course_info': course_info,
            'all_resources': all_resources,
            'lessons': lessons,
            'all_comment': all_comment
        })


class AddCourseComment(View):
    """
    添加评论
    """
    def post(self, request):
        course_id = request.POST.get('course_id', 0)
        comments = request.POST.get('comments', '')

        if not request.user.is_authenticated():
            return HttpResponse("{'status':'fail','msg':'用户未登陆'}", content_type='application/json')
        if int(course_id) > 0 and comments:
            course = Course.objects.get(id=int(course_id))
            course_comment = CourseComments()
            course_comment.comments = comments
            course_comment.course = course
            course_comment.user = request.user
            course_comment.save()
            return HttpResponse("{'status':'success','msg':'添加成功'}", content_type='application/json')
        else:
            return HttpResponse("{'status':'fail','msg':'添加失败'}", content_type='application.json')
