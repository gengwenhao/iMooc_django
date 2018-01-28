from datetime import datetime

from django.db import models

from organization.models import CourseOrg, Teacher


class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, verbose_name='所属课程机构', null=True)
    name = models.CharField(max_length=50, verbose_name='课程名称')
    desc = models.CharField(max_length=300, verbose_name='课程描述')
    detail = models.TextField(verbose_name='课程详情')
    teacher = models.ForeignKey(Teacher, verbose_name='讲师', null=True, blank=True)
    degree = models.CharField(choices=(('cj', '初级'), ('zj', '中级'), ('gj', '高级')), max_length=2, verbose_name='等级')
    is_banner = models.BooleanField(default=False, verbose_name='是否轮播')
    learn_times = models.IntegerField(default=0, verbose_name='学习时长(分钟数)')
    students = models.IntegerField(default=0, verbose_name='学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏人数')
    image = models.ImageField(upload_to='course/%Y/%m', verbose_name='封面图', max_length=100)
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    category = models.CharField(default='后端开发', max_length=20, verbose_name='课程类别')
    you_need_know = models.CharField(max_length=300, default='', verbose_name='课程须知')
    teacher_tell = models.CharField(max_length=300, default='', verbose_name='老师告诉你能学到什么')
    tag = models.CharField(default='', verbose_name='课程标签', max_length=10)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    # 获取学习用户
    def get_learn_users(self):
        return self.usercourse_set.all()[:5]

    def get_learn_users_nums(self):
        return self.usercourse_set.all().count()

    # 获取全部课程
    def get_course_lesson(self):
        all_lessons = self.lesson_set.all()

        return all_lessons

    # 获取课程章节数
    def get_zj_nums(self):
        all_lessons = self.lesson_set.all()
        lessons_nums = all_lessons.count()

        return lessons_nums


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name='课程')
    name = models.CharField(max_length=100, verbose_name='章节名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '章节'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    # 获取全部视频
    def get_all_video(self):
        all_video = self.video_set.all()

        return all_video


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name='章节')
    name = models.CharField(max_length=100, verbose_name='视频名称')
    url = models.CharField(max_length=200, default='', verbose_name='访问地址')
    learn_times = models.IntegerField(default=0, verbose_name='视频时长(分钟数)')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name='课程')
    name = models.CharField(max_length=100, verbose_name='名称')
    download = models.FileField(upload_to='course/resource/%Y/%m', verbose_name='资源文件', max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '课程资源'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
