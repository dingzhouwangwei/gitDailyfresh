from django.core.urlresolvers import reverse
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import View

from user.models import User,Address
import re,time
from dailyfresh2 import settings
from itsdangerous import TimedJSONWebSignatureSerializer
from django.contrib.auth import authenticate, login,logout

# Create your views here.
# class Register(View):
def register(request):
    if request.method=='GET':
    # def get(self,request):
        return render(request, 'register.html')
    # def post(self,request):
    if request.method=='POST':
        username = request.POST.get('user_name')
        userpwd = request.POST.get('pwd')
        cuserpwd = request.POST.get('cpwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')
        if not all([username, userpwd, email]):
            return render(request, 'register.html', {"msg": '输入不完整'})
        elif not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {"msg": '邮箱格式不正确'})
        elif userpwd != cuserpwd:
            return render(request, 'register.html', {"msg": '两次密码不一致'})
        elif allow != 'on':
            return render(request, 'register.html', {"msg": '请勾选协议'})
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None
        if user:
            return render(request, 'register.html', {"msg": '用户名已存在'})
        user = User.objects.create_user(username, email, password=userpwd)
        user.is_active = 0
        user.save()
        #todo 加密
        token={"user_id":user.id}
        ss=TimedJSONWebSignatureSerializer(settings.SECRET_KEY,3600)
        tt=ss.dumps(token)
        ss=tt.decode()
        #todo 发送邮件
        from celery_tasks.tasks import sent_register_active_mail
        sent_register_active_mail.delay(ss,email)
        return redirect(reverse('goods:index'))
# def active(request,str):
#     if request.method=='GET':
#         str = str.encode()
#         ss = tj(settings.SECRET_KEY, 3600)
#         str = ss.loads(str)
#         str = str.get('user_id')
#         user = User.objects.get(id=str)
#         user.is_active = 1
#         user.save()
#         # return redirect(reverse('goods:index'))
#         return redirect(reverse('goods:index'))
class Active(View):
    def get(self,request,str):
        str=str.encode()
        ss=TimedJSONWebSignatureSerializer(settings.SECRET_KEY,3600)
        str=ss.loads(str)
        str=str.get('user_id')
        user=User.objects.get(id=str)
        user.is_active=1
        user.save()
    # return redirect(reverse('goods:index'))
        return redirect(reverse('goods:index'))
class Login(View):
    def get(self,request):
        if 'username' in request.COOKIES:
            username=request.COOKIES.get('username')
            checked='checked'
        else:
            username=''
            checked=''
        return render(request,'login.html',{"usernaem":username,'checked':checked})
    def post(self,request):
        print('2')
        username=request.POST.get('username')
        pwd=request.POST.get('pwd')
        remember=request.POST.get('remember')
        if not all([username,pwd]):
            return render(request,'login.html',{"msg":'输入数据不完整'})
        user = authenticate(username=username, password=pwd)
        if user is not None:
            if user.is_active:
                login(request, user)
                res = redirect(reverse('goods:index'))
                if remember == "on":
                    res.set_cookie('username',username)
                else:
                    res.delete_cookie('username')
                return res
            else:
                return render(request, 'login.html', {"msg": '用户未激活，请到邮箱激活'})
        else:
            return render(request, 'login.html', {"msg": '用户名或密码不正确'})
class Logout(View):
    def get(self,request):
        logout(request)
        return redirect(reverse('user:login'))
class Info(View):
    def get(self,request):
        return render(request,'user_center_info.html' ,{"page":'info'})
class Order(View):
    def get(self,request):
        return render(request,'user_center_order.html',{"page":'order'})
class Addresss(View):
    def get(self,request):
        user=request.user
        address=Address.objects.get_default_address(user)
        return render(request,'user_center_site.html',{"page":"address",'address':address})
    def post(self,request):
        receiver=request.POST.get('receiver')
        addr=request.POST.get('addr')
        zip_code=request.POST.get('zip_code')
        phone=request.POST.get('phone')
        # print(receiver)
        if not all([receiver,addr,phone]):
            return render(request,'user_center_site.html',{"msg":'除邮编外其他必填'})
        if not re.match(r'^1[13578]\d{9}$',phone):
            return render(request,'user_center_site.html',{"msg":'电话格式不正确'})
        user=request.user
        address=Address.objects.get_default_address(user=user)
        if address:
            is_default=False
        else:
            is_default=True
        address=Address.objects.create(user=user,receiver=receiver,addr=addr,zip_code=zip_code,phone=phone,is_default=is_default)
        address.save()
        return redirect(reverse('user:address'))


