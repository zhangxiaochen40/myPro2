# _*_ coding:utf-8 _*_
from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse

from .models import CourseOrg, CityDict, Teacher
from .forms import UserAskForm
from operation.models import UserFavorite


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
        # 是否收藏
        has_fav = False
        # 判断用户是否收藏
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user,fav_id=course_org.id,fav_type=2):
                has_fav = True
        all_course = course_org.course_set.all()
        all_teacher = course_org.teacher_set.all()

        return render(request, 'org-detail-homepage.html', {
            'all_course': all_course,
            'all_teacher': all_teacher,
            'current_page': current_page,
            'course_org': course_org,
            'has_fav': has_fav
        })


class OrgCourseView(View):
    """
    课程详情
    """
    def get(self, request, org_id):
        current_page = 'course'
        course_org = CourseOrg.objects.get(id=int(org_id))
        # 判断用户是否收藏
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user,fav_id=course_org.id,fav_type=2):
                has_fav = True
        all_course = course_org.course_set.all()

        return render(request, 'org-detail-course.html', {
            'all_course': all_course,
            'current_page': current_page,
            'course_org': course_org,
            'has_fav': has_fav
        })


class OrgDescView(View):
    """
    机构详情页
    """

    def get(self, request, org_id):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user,fav_id=course_org.id,fav_type=2):
                has_fav = True
        return render(request, 'org-detail-desc.html', {
            'current_page': current_page,
            'course_org': course_org,
            'has_fav': has_fav
        })


class OrgTeacherView(View):
    """教师详情"""

    def get(self, request, org_id):
        current_page = 'teacher'
        course_org = CourseOrg.objects.get(id=int(org_id))

        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user,fav_id=course_org.id,fav_type=2):
                has_fav = True

        all_course = course_org.course_set.all()
        all_teacher = course_org.teacher_set.all()

        return render(request, 'org-detail-teachers.html', {
            'all_course': all_course,
            'all_teacher': all_teacher,
            'current_page': current_page,
            'course_org': course_org,
            'has_fav': has_fav
        })


class AddFavView(View):
    """
    用户收藏，用户取消收藏
    """
    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)

        if not request.user.is_authenticated():
            '''用户未登陆'''
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')

        exist_record = UserFavorite.objects.filter(user=request.user,fav_id=int(fav_id),fav_type=int(fav_type))
        if exist_record:
            '''如果存在记录，代表以收藏则删除收藏信息'''
            exist_record.delete()
            return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')
        if int(fav_id) > 0 and int(fav_type) > 0:
            user_fav = UserFavorite()
            user_fav.user = request.user
            user_fav.fav_id = int(fav_id)
            user_fav.fav_type = int(fav_type)
            user_fav.save()
            return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"success", "msg":"收藏出错"}', content_type='application/json')


class TeacherListView(View):
    """教师列表展示"""
    def get(self, request):

        all_teachers = Teacher.objects.all()
        # 排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'hot':
                all_teachers = all_teachers.order_by('-click_nums')
        # 热门教师
        hot_teachers = Teacher.objects.all().order_by('-click_nums')[:3]
        # 教师列表分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_teachers, 3, request=request)

        teachers = p.page(page)

        # 教师列表分页
        return render(request, 'teachers-list.html', {
            'all_teachers': teachers,
            'hot_teachers': hot_teachers,
            'sort': sort
        })
