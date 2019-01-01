# _*_ coding:utf-8 _*_
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from webtest.models import Event
# Create your views here.
#登录逻辑
def index(request):
    return render(request,"index.html")
def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            response = HttpResponseRedirect('/event_manage/')
#           response.set_cookie('user',username,3600)
            request.session['user']=username
            return response
        else:
            return render(request,'index.html',{"error":u"用户名或密码错误!"})
    else:
        return HttpResponse(u"请求方法错误")
#登陆成功后返回
@login_required
def event_manage(request):
    #realname=request.COOKIES.get('user','')
    #realname=request.session.get('user','')
    #return render(request,"event_manage.html",{'user':realname})
    event_list=Event.objects.all()
    username=request.session.get('user','')
    return  render(request,'event_manage.html',{'user':username,'events':event_list})
