from django.core.urlresolvers import reverse
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from user.models import User
import re,time
from dailyfresh2 import settings
from itsdangerous import TimedJSONWebSignatureSerializer as tj

# Create your views here.
def register(request,):
    if request.method=='GET':
        return render(request,'register.html')
    if request.method=='POST':
        username=request.POST.get('user_name')
        userpwd=request.POST.get('pwd')
        cuserpwd=request.POST.get('cpwd')
        email=request.POST.get('email')
        allow=request.POST.get('allow')
        if not all([username,userpwd,email]):
            return render(request,'register.html',{"msg":"请填写完整"})
        if userpwd != cuserpwd:
            return render(request, 'register.html', {"msg": "前后密码不一致"})
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$',email):
            return render(request, 'register.html', {"msg": "邮箱格式不正确"})
        if allow !='on':
            return render(request, 'register.html', {"msg": "请同意协议"})
        try:
            user=User.objects.get(username=username)
        except Exception:
            user=None
        if user:
            return render(request, 'register.html', {"msg": "此用户已注册"})
        user=User.objects.create_user(username,userpwd,email)
        user.is_active=0
        user.save()
        #todo 加密
        tt=tj(settings.SECRET_KEY,3600)
        token={"user_id":user.id}
        ss=tt.dumps(token)
        ss=ss.decode()
        #todo 发送邮件
        from celery_tasks.tasks import sent_register_active_mail
        sent_register_active_mail.delay(ss,email)
def active(request,str):
    print(str)
    tt=tj(settings.SECRET_KEY,3600)
    str=str.encode()
    ss=tt.loads(str)
    id=ss.get('user_id')
    print(id)
    user=User.objects.get(id=id)
    user.is_active=1
    user.save()
    return redirect(reverse('goods:index'))

