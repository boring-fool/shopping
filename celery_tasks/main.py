from celery import Celery
import os

if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'shopping.settings.dev'
#创建celery实例
celery_app = Celery('shopping')
#加载配置
celery_app.config_from_object('celery_tasks.config')
#注册任务
celery_app.autodiscover_tasks(['celery_tasks.sms','celery_tasks.email'])