from django.shortcuts import render, HttpResponse
from django.views.generic.base import View
from django.db.models import Q
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import *
from operation.models import UserFavourite, CourseComments, UserCourse
from utils.mixin_utils import LoginRequiredMixin


# 课程列表
class CourseListView(View):
    def get(self, request):
        cur_nav = 'course'

        all_courses = Course.objects.all().order_by('-add_time')

        hot_courses = Course.objects.all().order_by('-click_nums')[:3]

        # 课程搜索
        search_keywords = request.GET.get('keywords', '')

        if search_keywords:
            all_courses = all_courses.filter(
                Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords) | Q(
                    detail__icontains=search_keywords))

        # 排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_courses = all_courses.order_by('-students')

            elif sort == 'hot':
                all_courses = all_courses.order_by('-click_nums')

        # 对课程进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, 9, request=request)

        org_nums = all_courses.count()

        all_courses = p.page(page)

        return render(request, 'course-list.html', locals())


# 课程详情
class CourseDetailView(View):
    def get(self, request, course_id):
        course_has_fav = False
        course_org_has_fav = False

        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        if request.user.is_authenticated():
            if UserFavourite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                course_has_fav = True
            if UserFavourite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                course_org_has_fav = True

        tag = course.tag
        if tag:
            relate_courses = Course.objects.filter(tag=tag)[:1]
        else:
            relate_courses = []

        return render(request, 'course-detail.html', locals())


# 课程章节信息
class CourseInfoView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_resource = CourseResource.objects.filter(course=course)

        # 查询用户是否已经关联了该课程
        user_courses = UserCourse.objects.filter(user=request.user, course_id=course_id)
        if not user_courses:
            user_course = UserCourse(user=request.user, course_id=course_id)
            user_course.save()

        # 获取该课程的所有学员
        user_courses = UserCourse.objects.filter(course=course)

        # 取出所有学员的id
        user_ids = [user_course.user_id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)

        # 取出所有课程id
        course_ids = [user_course.course.id for user_course in all_user_courses]

        # 获取该课程的同学还学过的课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]

        return render(request, 'course-video.html', locals())


# 课程评论
class CommentView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_comments = CourseComments.objects.filter(course=course)[:10]
        all_resource = CourseResource.objects.filter(course=course)
        # 获取该课程的所有学员
        user_courses = UserCourse.objects.filter(course=course)

        # 取出所有学员的id
        user_ids = [user_course.user_id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)

        # 取出所有课程id
        course_ids = [user_course.course.id for user_course in all_user_courses]

        # 获取该课程的同学还学过的课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]

        return render(request, 'course-comment.html', locals())


class AddCommentView(View):
    def post(self, request):
        # 判断用户登陆状态
        if not request.user.is_authenticated():

            return HttpResponse('{"status":"fail", "msg":"用户未登陆"}', content_type='application/json')
        else:
            user = request.user
            course_id = int(request.POST.get('course_id', 0))
            comments = request.POST.get('comments', '')
            if course_id > 0 and comments:
                try:
                    CourseComments.objects.create(user=user, course_id=course_id, comments=comments)
                except:
                    return HttpResponse('{"status":"fail", "msg":"出错"}', content_type='application/json')

                return HttpResponse('{"status":"success", "msg":"评论成功"}', content_type='application/json')


class VideoPlayView(View):
    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.lesson.course
        all_comments = CourseComments.objects.filter(course=course)[:10]
        all_resource = CourseResource.objects.filter(course=course)
        # 获取该课程的所有学员
        user_courses = UserCourse.objects.filter(course=course)

        # 取出所有学员的id
        user_ids = [user_course.user_id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)

        # 取出所有课程id
        course_ids = [user_course.course.id for user_course in all_user_courses]

        # 获取该课程的同学还学过的课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]

        return render(request, 'course-play.html', locals())
