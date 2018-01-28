from django.contrib import admin

from .models import *


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('nick_name', 'username', 'birthday', 'gender', 'address', 'mobile', 'image')
    list_filter = ('nick_name', 'username', 'gender', 'address', 'mobile')
    search_fields = ('nick_name', 'gender', 'address', 'mobile')


@admin.register(EmailVerifyRecord)
class EmailVerifyRecordAdmin(admin.ModelAdmin):
    pass


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    pass
