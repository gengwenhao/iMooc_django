import json

from django.shortcuts import render, HttpResponse, HttpResponseRedirect, reverse
# 导入django内置的用户验证和登陆模块
from django.contrib.auth import authenticate, login as login_inner, logout
# 导入django内置验证模块的模板, 用于自定制验证方式
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
# 导入django视图函数的基类
from django.views.generic.base import View
# 导入django内置的密码哈希函数
from django.contrib.auth.hashers import make_password
from pure_pagination import Paginator, PageNotAnInteger

from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin
from utils.send_message import send_message
from .models import *
from operation.models import UserCourse, UserFavourite, UserMessage
from course.models import Course
from organization.models import CourseOrg, Teacher
from .forms import *


# 全局404处理函数
def page_not_found(request):
    from django.shortcuts import render_to_response
    response = render_to_response('404.html')
    response.status_code = 404

    return response


# 全局500处理函数
def page_error(request):
    from django.shortcuts import render_to_response
    response = render_to_response('500.html')
    response.status_code = 500

    return response


# 重定义用户验证模块
class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            # 根据用户名或邮箱查找用户
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            # 验证密码
            if user.check_password(password):
                # 通过返回用户
                return user
            else:
                # 不通过返回空
                return None

        # 异常返回空
        except Exception as e:
            return None


# 修改密码
class ResetView(View):
    def get(self, request, reset_code):
        # 根据激修改查找对应的邮箱
        all_records = EmailVerifyRecord.objects.filter(code=reset_code)
        # 如果查到修改码对应的邮箱
        if all_records:
            for record in all_records:
                modify_pwd_form = ModifyPwdForm()
                email = record.email
                return render(request, 'password_reset.html', locals())
        else:
            return render(request, '404.html')


# 修改密码
class ModifyPwdView(View):
    def post(self, request):
        modify_pwd_form = ModifyPwdForm(request.POST)
        if modify_pwd_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')
            if pwd1 != pwd2:
                msg = '两次输入的密码不相同'
                return render(request, 'password_reset.html', locals())
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()

            return render(request, 'login.html')

        else:
            msg = ''
            return render(request, 'password_reset.html', locals())


# 忘记密码
class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html', locals())

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            send_register_email(email, 'forget')
            return HttpResponse('邮件已发送, 请查收')
        else:
            return render(request, 'forgetpwd.html', locals())


# 激活用户
class ActiveUserView(View):
    # 页面get请求后直接查找激活码并激活对应账户
    def get(self, request, active_code):
        # 根据激活码查找对应的邮箱
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        # 如果查到激活码对应的邮箱
        if all_records:
            # 遍历所有符合条件的邮箱
            for record in all_records:
                record_email = record.email
                # 查找邮箱绑定的账户
                user = UserProfile.objects.get(email=record_email)
                # 激活账户
                user.is_active = True
                user.save()
        else:
            return render(request, '404.html')

        return render(request, 'login.html')


# 注册用户
class RegisterView(View):
    # get请求返回注册页面
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', locals())

    # post请求, 验证提交的表单
    def post(self, request):
        welcome_str_after_register = '欢迎注册'

        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email', '')
            if UserProfile.objects.filter(email=user_name):
                msg = '用户名已存在'
                return render(request, 'register.html', locals())
            pass_word = request.POST.get('password', '')

            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            # 使用django内置的哈希模块加密密码
            user_profile.password = make_password(pass_word)
            user_profile.save()

            send_message(
                user=user_profile,
                msg='欢迎您的注册!'
            )

            # 发送激活连接给邮箱
            msg = send_register_email(user_name, 'register')
            return render(request, 'login.html', locals())

        else:
            return render(request, 'register.html', locals())


# 登陆验证
class LoginView(View):
    # get请求返回登陆页面
    def get(self, request):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('index'))

        return render(request, 'login.html', locals())

    # post请求, 验证提交的表单
    def post(self, request):
        login_form = LoginForm(request.POST)

        # check form
        if login_form.is_valid():
            target_username = request.POST.get('username', '')
            target_password = request.POST.get('password', '')

            user = authenticate(
                username=target_username,
                password=target_password
            )

            # check is_active
            if user:
                msg = ''
                if user.is_active:
                    login_inner(request, user)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    msg = '用户待激活, 检查邮箱'
                    return render(request, 'login.html', locals())
            else:
                msg = '用户不存在'
                return render(request, 'login.html', locals())

        # not login_form.is_valid()
        else:
            return render(request, 'login.html', locals())


# 登陆退出
class LogoutView(View):
    def get(self, request):
        logout(request)
        from django.core.urlresolvers import reverse

        return HttpResponseRedirect(reverse('index'))


# 个人资料
class UserInfoView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'usercenter-info.html', locals())

    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()

            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


# 我的课程
class MyCourseView(LoginRequiredMixin, View):
    def get(self, request):
        cur_user = request.user
        my_all_courses = (course.course for course in UserCourse.objects.filter(user=cur_user))

        return render(request, 'usercenter-mycourse.html', locals())


# 我的收藏课程
class FavCourseView(LoginRequiredMixin, View):
    def get(self, request):
        cur_user = request.user
        all_fav_ids = (obj.fav_id for obj in UserFavourite.objects.filter(user=cur_user, fav_type=1))
        all_fav_courses = (Course.objects.get(id=fav_id) for fav_id in all_fav_ids)

        return render(request, 'usercenter-fav-course.html', locals())


# 我的收藏机构
class FavOrgView(LoginRequiredMixin, View):
    def get(self, request):
        cur_user = request.user
        all_fav_ids = (obj.fav_id for obj in UserFavourite.objects.filter(user=cur_user, fav_type=2))
        all_fav_org = (CourseOrg.objects.get(id=fav_id) for fav_id in all_fav_ids)

        return render(request, 'usercenter-fav-org.html', locals())


# 我的收藏教师
class FavTeacherView(LoginRequiredMixin, View):
    def get(self, request):
        cur_user = request.user
        all_fav_ids = (obj.fav_id for obj in UserFavourite.objects.filter(user=cur_user, fav_type=3))
        all_fav_teacher = (Teacher.objects.get(id=fav_id) for fav_id in all_fav_ids)

        return render(request, 'usercenter-fav-teacher.html', locals())


# 我的消息中心
class CenterMsgView(LoginRequiredMixin, View):
    def get(self, request):
        cur_user = request.user
        all_my_messages = UserMessage.objects.filter(user=cur_user.id, has_read=False)

        # 进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_my_messages, 3, request=request)

        all_my_messages = p.page(page)

        return render(request, 'usercenter-message.html', locals())


# 用户头像修改
class UploadImageView(LoginRequiredMixin, View):
    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()

            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


# 个人中心修改密码
class UpdatePwdView(View):
    def post(self, request):
        modify_pwd_form = ModifyPwdForm(request.POST)
        if modify_pwd_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            if pwd1 != pwd2:
                msg = '两次输入的密码不相同'
                return HttpResponse('{"status":"fail", "msg":"两次密码不一致"}', content_type='application/json')
            user = request.user
            user.password = make_password(pwd2)
            user.save()

            return HttpResponse('{"status":"success"}', content_type='application/json')

        else:
            return HttpResponse(json.dumps(modify_pwd_form.errors), content_type='application/json')


# 向新邮箱发送验证码
class SendNewEmailCodeView(LoginRequiredMixin, View):
    def get(self, request):
        new_email = request.GET.get('email', '')

        if UserProfile.objects.filter(email=new_email):
            return HttpResponse('{"email":"邮箱已经存在"}', content_type='application/json')

        send_register_email(email=new_email, send_type='update_email')
        return HttpResponse('{"status":"success"}', content_type='application/json')


# 修改邮箱
class UpdateEmailView(LoginRequiredMixin, View):
    def post(self, request):
        target_email = request.POST.get('email', '')
        target_code = request.POST.get('code', '')

        existed_records = EmailVerifyRecord.objects.filter(
            email=target_email,
            code=target_code,
            send_type='update_email'
        )

        if existed_records:
            user = request.user
            user.email = target_email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"您输入的验证码有误!"}', content_type='application/json')
