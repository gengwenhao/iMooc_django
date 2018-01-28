from django.contrib import admin

from organization.models import *


@admin.register(CityDict)
class CityDictAdmin(admin.ModelAdmin):
    pass


@admin.register(CourseOrg)
class CourseOrgAdmin(admin.ModelAdmin):
    pass


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    pass
