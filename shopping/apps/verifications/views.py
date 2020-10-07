from django.shortcuts import render
from django.views import View
from django_redis import get_redis_connection
from django.http import HttpResponse
from shopping.apps.verifications.libs.captcha import captcha
from .constants import IMAGE_CODE_REDIS_EXPIRES
# Create your views here.

class ImageCodeView(View):
    def get(self,request,uuid):
        text,image = captcha.captcha.generate_captcha()
        redis_conn = get_redis_connection('verify_code')
        redis_conn.setex('img_{}'.format(uuid),IMAGE_CODE_REDIS_EXPIRES,text)
        return HttpResponse(image,content_type='image/jpg')
