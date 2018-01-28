from django.contrib import admin

from operation.models import *


@admin.register(UserAsk)
class UserAskAdmin(admin.ModelAdmin):
    pass


@admin.register(CourseComments)
class CourseCommentsAdmin(admin.ModelAdmin):
    pass


@admin.register(UserFavourite)
class UserFavouriteAdmin(admin.ModelAdmin):
    pass


@admin.register(UserMessage)
class UserMessageAdmin(admin.ModelAdmin):
    pass


@admin.register(UserCourse)
class UserCourseAdmin(admin.ModelAdmin):
    pass
