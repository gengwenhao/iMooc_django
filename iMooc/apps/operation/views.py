from django.shortcuts import render, HttpResponse
from django.views.generic.base import View

from .forms import UserAskForm


# Create your views here.
class AddUserAskView(View):
    # 用户添加咨询
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            return HttpResponse("{'status':'success'}", content_type='application/json')
        else:
            return HttpResponse("{'status':'fail', 'msg':'添加出错'}", content_type='application/json')
