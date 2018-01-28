from django.contrib import admin

from course.models import *


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    pass


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    pass


@admin.register(CourseResource)
class CourseResourceAdmin(admin.ModelAdmin):
    pass
