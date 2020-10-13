import random,logging
from django.views import View
from django_redis import get_redis_connection
from django.http import HttpResponse,JsonResponse,HttpResponseForbidden

from shopping.apps.verifications.libs.captcha import captcha
from shopping.utils.response_code import RETCODE
from shopping.apps.verifications import constants
from celery_tasks.sms.tasks import send_sms_code
# from shopping.celery_tasks.sms.message import CCP

# Create your views here.
logger = logging.getLogger('django')
class ImageCodeView(View):
    def get(self,request,uuid):
        text,image = captcha.captcha.generate_captcha()
        redis_conn = get_redis_connection('verify_code')
        redis_conn.setex('img_{}'.format(uuid),constants.IMAGE_CODE_REDIS_EXPIRES,text)
        return HttpResponse(image,content_type='image/jpg')

class SMSCodeView(View):
    def get(self,request,mobile):
        image_code_client = request.GET.get('image_code')
        uuid = request.GET.get('uuid')
        if not all([image_code_client,uuid]):
            return HttpResponseForbidden('缺少必传参数')
        redis_conn = get_redis_connection('verify_code')
        image_code_server = redis_conn.get('img_{}'.format(uuid)) #bytes类型
        if not image_code_server:
            return JsonResponse({'code':RETCODE.IMAGECODEERR,'errmsg':'图形验证码已失效'})
        redis_conn.delete('img_{}'.format(uuid))
        image_code_server = image_code_server.decode()
        if image_code_server.lower() !=image_code_client.lower():
            return JsonResponse({'code':RETCODE.IMAGECODEERR,'errmsg':'输入图形验证码有误'})
        if redis_conn.get('msg_{}'.format(mobile)):
            return JsonResponse({'code':RETCODE.THROTTLINGERR,'errmsg':'发送短信过于频繁'})
        msg_code = '{:0>6d}'.format(random.randint(0,999999))
        logger.info(msg_code)
        redis_conn.setex('msg_{}'.format(mobile),constants.IMAGE_CODE_REDIS_EXPIRES,msg_code)
        send_sms_code.delay(mobile,msg_code)
        # CCP().send_message(constants.SEND_SMS_TEMPLATE_ID,mobile,(msg_code,constants.SMS_CODE_REDIS_EXPIRES//60))
        return JsonResponse({'code':RETCODE.OK,'errmsg':'发送短信成功'})

