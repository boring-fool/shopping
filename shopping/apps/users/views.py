import re,json,logging
from django import http
from django.urls import reverse
from django.db import DatabaseError
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render,redirect
from django.views import View
from django_redis import get_redis_connection

from .models import User
from shopping.utils.response_code import RETCODE
from shopping.utils.views import LoginJsonMixin
from celery_tasks.email.tasks import send_verify_email
from .utils import generate_verify_email_url, check_verify_email_token
# Create your views here.

logger = logging.getLogger('django')
class UsernameCountView(View):
    def get(self,request,username):
        # 使用username查询对应的记录的条数(filter返回的是满足条件的结果集)
        count = User.objects.filter(username=username).count()
        # 响应结果
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'count': count})
class MobileCountView(View):
    def get(self,request,mobile):
        count = User.objects.filter(mobile=mobile).count()
        return http.JsonResponse({'code':RETCODE.OK,'errmsg': 'OK', 'count': count})

class LoginView(View):
    def get(self,request):
        return render(request,'login.html')
    def post(self,request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        remembered = request.POST.get('remembered')
        if not all([username,password]):
            return http.HttpResponseForbidden('缺少必传参数')
        #判断用户名输入是否正确
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return http.HttpResponseForbidden('请输入正确的用户名或手机号')
        # 判断密码是否是8-20个数字
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return http.HttpResponseForbidden('请输入8-20位的密码')
        user = authenticate(username=username,password=password)
        if not user:
            return render(request,'login.html',{'account_errmsg':'请输入正确的账户密码'})
        login(request,user)
        if remembered!= 'on':
            request.session.set_expiry(0)  # 单位是秒
        else:
        # 记住登录：状态保持周期为两周:默认是两周
            request.session.set_expiry(None)
        next = request.GET.get('next')
        if next:
            response = redirect(next)
        else:
            response = redirect(reverse('contents:index'))
        response.set_cookie('username',user.username,max_age=3600*24*14)
        return response

class LogoutView(View):
    def get(self,request):
        logout(request)
        response = redirect(reverse('contents:index'))
        response.delete_cookie('username')
        return response

class RegisterView(View):
    def get(self,request):
        return render(request,'register.html')

    def post(self,request):
        """实现用户注册业务逻辑"""
        # 接收参数：表单参数
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        mobile = request.POST.get('mobile')
        allow = request.POST.get('allow')
        sms_code_client = request.POST.get('sms_code')

        # 校验参数：前后端的校验需要分开，避免恶意用户越过前端逻辑发请求，要保证后端的安全，前后端的校验逻辑相同
        # 判断参数是否齐全:all([列表])：会去校验列表中的元素是否为空，只要有一个为空，返回false
        if not all([username, password, password2, mobile, allow]):
            return http.HttpResponseForbidden('缺少必传参数')
        # 判断用户名是否是5-20个字符
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return http.HttpResponseForbidden('请输入5-20个字符的用户名')
        # 判断密码是否是8-20个数字
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return http.HttpResponseForbidden('请输入8-20位的密码')
        # 判断两次密码是否一致
        if password != password2:
            return http.HttpResponseForbidden('两次输入的密码不一致')
        # 判断手机号是否合法
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return http.HttpResponseForbidden('请输入正确的手机号码')
        #判断短信验证码
        redis_conn = get_redis_connection('verify_code')
        sms_code_server = redis_conn.get('msg_{}'.format(mobile))
        if  not sms_code_server:
            return render(request,'register.html',{'sms_code_errmsg':'验证码已失效'})
        if sms_code_server.decode() != sms_code_client:
            return render(request,'register.html',{'sms_code_errmsg':'验证码输入错误'})
        # 判断是否勾选用户协议
        if allow != 'on':
            return http.HttpResponseForbidden('请勾选用户协议')

        # 保存注册数据

        try:
            user = User.objects.create_user(username=username, password=password, mobile=mobile)
        except DatabaseError:
            return render(request, 'register.html', {'sms_code_errmsg': '注册失败'})

        # 实现状态保持

        login(request,user)

        # 响应结果：重定向到首页
        # return http.HttpResponse('注册成功，重定向到首页')

        return redirect(reverse('contents:index'))
class UserInfoView(LoginRequiredMixin,View):
    def get(self,request):
        context = {
            'username' : request.user.username,
            'mobile' : request.user.mobile,
            'email' : request.user.email,
            'email_active' : request.user.email_active,
        }
        return render(request,'user_center_info.html',context)

class VerifyEmailView(View):
    """验证邮箱"""

    def get(self, request):
        # 接收参数
        token = request.GET.get('token')

        # 校验参数
        if not token:
            return http.HttpResponseForbidden('缺少token')

        # 从token中提取用户信息user_id ==> user
        user = check_verify_email_token(token)
        if not user:
            return http.HttpResponseBadRequest('无效的token')

        # 将用户的email_active字段设置为True
        try:
            user.email_active = True
            user.save()
        except Exception as e:
            logger.error(e)
            return http.HttpResponseServerError('激活邮箱失败')

        # 响应结果：重定向到用户中心
        return redirect(reverse('users:info'))

class EmailView(LoginJsonMixin,View):
    def put(self,request):
        email_str = request.body.decode()
        email_dict = json.loads(email_str)
        email = email_dict.get('email')
        if not re.match('^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$',email):
            return http.HttpResponseForbidden('请输入的邮箱地址')
        try:
            request.user.email = email
            request.user.save()
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code':RETCODE.DBERR,'errmsg':'添加邮箱失败'})
        # 发送邮箱验证邮件
        verify_url = generate_verify_email_url(request.user)
        # send_verify_email(email, verify_url) # 错误的写法
        send_verify_email.delay(email, verify_url)  # 一定要记得调用delay

        # 响应结果

        return http.JsonResponse({'code':RETCODE.OK,'errmsg':'OK'})
class AddressView(LoginRequiredMixin, View):
    """用户收货地址"""
    def get(self, request):
        return render(request, 'user_center_site.html')


