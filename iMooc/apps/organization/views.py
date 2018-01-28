from django.shortcuts import render, HttpResponse, HttpResponseRedirect, reverse
from django.views.generic.base import View
from django.db.models import Q
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import *
from operation.forms import UserAskForm
from operation.models import *
from course.models import Course
from user.models import Banner


# 首页
class IndexView(View):
    def get(self, request):
        cur_nav = 'index'
        # 取出轮播图
        all_banners = Banner.objects.all().order_by('index')
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        course_orgs = CourseOrg.objects.all()[:15]

        return render(request, 'index.html', locals())


# 机构列表页面
class OrgView(View):
    def get(self, request):
        cur_nav = 'org'

        # 课程机构
        all_orgs = CourseOrg.objects.all()

        hot_orgs = all_orgs.order_by('click_nums')[:3]

        # 城市
        all_citys = CityDict.objects.all()

        # 机构搜索
        search_keywords = request.GET.get('keywords', '')

        if search_keywords:
            all_orgs = all_orgs.filter(
                Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords))
        # 类别筛选
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category=category)

        # 排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_orgs = all_orgs.order_by('-click_nums')

            elif sort == 'courses':
                all_orgs = all_orgs.order_by('-course_nums')

        # 取出筛选城市
        city_id = request.GET.get('city', '')
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        # 对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_orgs, 4, request=request)

        org_nums = all_orgs.count()

        all_orgs = p.page(page)

        return render(request, 'org-list.html', locals())


# 机构首页
class OrgHomeView(View):
    def get(self, request, org_id):
        current_page = 'home'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavourite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:1]

        return render(request, 'org-detail-homepage.html', locals())


# 机构课程列表页面
class OrgCourseView(View):
    def get(self, request, org_id):
        current_page = 'course'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()[:3]

        return render(request, 'org-detail-course.html', locals())


# 机构描述页
class OrgDescView(View):
    def get(self, request, org_id):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id=int(org_id))

        return render(request, 'org-detail-desc.html', locals())


# 机构教师页
class OrgTeacherView(View):
    def get(self, request, org_id):
        current_page = 'teacher'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teachers = course_org.teacher_set.all()[:3]

        return render(request, 'org-detail-teachers.html', locals())


class AddFavView(View):
    # 用户收藏
    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)

        if not request.user.is_authenticated():
            # 判断用户登陆状态
            return HttpResponse('{"status":"fail", "msg":"用户未登陆"}', content_type='application/json')

        exist_records = UserFavourite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        # 如果记录已经存在则表示用户取消收藏
        if exist_records:
            exist_records.delete()
            return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')
        else:
            user_fav = UserFavourite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()
                return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')


# 课程讲师列表页
class TeacherListView(View):
    def get(self, request):
        # 当前导航页
        cur_nav = 'teacher'
        # 排序规则
        sort = request.GET.get('sort', '')

        all_teachers = Teacher.objects.all()
        # 统计老师总数
        teachers_count = all_teachers.count()
        # 筛选出收藏最多的签3名老师作为讲师排行榜
        fav_teachers = all_teachers.order_by('fav_nums')[:3]

        if sort == 'hot':
            all_teachers = all_teachers.order_by('-click_nums')

        # 老师搜索
        search_keywords = request.GET.get('keywords', '')

        if search_keywords:
            all_teachers = all_teachers.filter(name__icontains=search_keywords)

        # 对课教师列表进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_teachers, 3, request=request)

        all_teachers = p.page(page)

        return render(request, 'teachers-list.html', locals())


class TeacherDetail(View):
    def get(self, request, teacher_id):
        if request.user.is_authenticated():
            is_fav_teacher = False
            is_fav_org = False

            teacher = Teacher.objects.get(id=int(teacher_id))

            exist_record_teacher = UserFavourite.objects.filter(user=request.user, fav_id=int(teacher_id),
                                                                fav_type=int(3))
            exist_record_org = UserFavourite.objects.filter(user=request.user, fav_id=int(teacher.org.id),
                                                            fav_type=int(2))
            if exist_record_teacher:
                is_fav_teacher = True
            if exist_record_org:
                is_fav_org = True

            all_courses = teacher.course_set.all()[:10]
            return render(request, 'teacher-detail.html', locals())
        else:
            return HttpResponseRedirect(reverse('login'))
