# _*_ coding:utf-8 _*_
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from webtest.models import Event,Guest
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
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

#搜索
@login_required
def search_name(request):
    username=request.session.get('user','')
    search_name=request.GET.get('name','')
    event_list=Event.objects.filter(name__contains=search_name)
    return  render(request,'event_manage.html',{'user':username,'events':event_list})

#guest管理
@login_required
def guest_manage(request):
    username=request.session.get('user','')
    guest_list=Guest.objects.all()
    paginator=Paginator(guest_list,2)
    ww=request.GET.get('page')
    try:
        contacts= paginator.page(ww)
    except PageNotAnInteger:
        #如果page不是整数，取第一个页面的数据
        contacts=paginator.page(1)
    except EmptyPage:
        #如果page不在范围，取最后一页面
        contacts=paginator.page(paginator.num_pages)
    return render(request,'guest_manage.html',{'user':username,'guests':contacts})

#guest搜索表单
@login_required
def search_realname(request):
    username=request.session.get('user','')
    search_name=request.GET.get('realname','')
    guest_list=Guest.objects.filter(realname__contains=search_name)
    return  render(request,'guest_manage.html',{'user':username,'guests':guest_list })

#签到页面
@login_required
def sign_index(request,eid):
    event=get_object_or_404(Event,id=eid)
    return render(request,'sign_index.html',{'events':event})

#签到动作
@login_required
def sign_index_action(request,eid):
    event=get_object_or_404(Event,id=eid)
    phone=request.GET.get('phone','')
    print (phone)
    result=Guest.objects.filter(phone=phone)
    if not result:
        return render(request,'sign_index.html',{'event':event,'hint':'phone error'})
    result=Guest.objects.filter(phone=phone,event_id=eid)
    if not result:
        return render(request,'sign_index.html',{'event':event,'hint':'event id or phone error'})
    result=Guest.objects.get(phone=phone,event_id=eid)
    if result.sign:
        return  render(request,'sign_index.html',{'event':event,'hint':"user has sign in"})
    else:
        Guest.objects.filter(phone=phone,event_id=eid).update(sign='1')
        return render(request,'sign_index.html',{'event':event,'hint':'sign in success!','guest':result})