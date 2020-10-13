
from .message import CCP
from . import constants
from ..main import celery_app

# 使用装饰器装饰异步任务，保证celery识别任务
@celery_app.task(bind=True,name='send_sms_code',retry_backoff=3)
def send_sms_code(self,mobile, msg_code):
    """
    发送短信验证码的异步任务
    :param mobile: 手机号
    :param sms_code: 短信验证码
    :return: 成功：0 、 失败：-1
    """
    try:
        send_ret = CCP().send_message(constants.SEND_SMS_TEMPLATE_ID, mobile, (msg_code,
                                                                       constants.SMS_CODE_REDIS_EXPIRES // 60))
    except Exception as e:
        raise self.retry(exc=e, max_retries=3)

    return send_ret