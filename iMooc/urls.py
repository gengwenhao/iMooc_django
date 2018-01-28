"""iMooc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.views.static import serve
import xadmin

from user.views import *
from organization.views import *

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^logout/', LogoutView.as_view(), name='logout'),
    url(r'^register/', RegisterView.as_view(), name='register'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/', ActiveUserView.as_view(), name='user_active'),
    url(r'^forget/', ForgetPwdView.as_view(), name='forget'),
    url(r'^reset/(?P<reset_code>.*)/', ResetView.as_view(), name='reset'),
    url(r'^modify_pwd/', ModifyPwdView.as_view(), name='modify_pwd'),

    # 课程机构url配置
    url(r'^org/', include('organization.urls', namespace='org')),
    # 课程url配置
    url(r'^course/', include('course.urls', namespace='course')),
    # 讲师url配置
    url(r'^teacher/', include('organization.urls', namespace='teacher')),
    # 用户url配置
    url(r'^users/', include('user.urls', namespace='user')),
    # 配置上传文件的访问处理函数
    url(r'^media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT}),
    # 配置静态资源的访问处理函数
    url(r'^static/(?P<path>.*)', serve, {'document_root': settings.STATIC_ROOT}),
]
# 全局404页面配置
hander404 = 'users.views.page_not_found'
# 全局500页面配置
hander500 = 'users.views.page_error'
