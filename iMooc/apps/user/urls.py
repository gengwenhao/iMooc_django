from django.conf.urls import url

from .views import *

urlpatterns = [
    # 个人资料
    url(r'^info/$', UserInfoView.as_view(), name='user_info'),
    # 我的课程
    url(r'^mycourse/$', MyCourseView.as_view(), name='mycourse'),
    # 我的收藏课程
    url(r'^fav_course/$', FavCourseView.as_view(), name='fav_course'),
    # 我的收藏机构
    url(r'^fav_org/$', FavOrgView.as_view(), name='fav_org'),
    # 我的收藏教师
    url(r'^fav_teacher/$', FavTeacherView.as_view(), name='fav_teacher'),
    # 我的消息
    url(r'^center_msg/$', CenterMsgView.as_view(), name='center_msg'),

    # 用户头像上传
    url(r'^image/upload/$', UploadImageView.as_view(), name='image_upload'),
    # 用户个人中心修改密码
    url(r'^update/pwd/$', UpdatePwdView.as_view(), name='update_pwd'),
    # 向新邮箱发送验证码
    url(r'^send_new_email_code/$', SendNewEmailCodeView.as_view(), name='send_new_email_code'),
    # 修改新邮箱
    url(r'^update_email/$', UpdateEmailView.as_view(), name='update_email'),
]
