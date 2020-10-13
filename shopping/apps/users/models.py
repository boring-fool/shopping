from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    mobile = models.CharField(unique=True,max_length=12,verbose_name='手机号')
    email_active = models.BooleanField(default=False,verbose_name='邮箱验证状态')
    class Meta:
        db_table = 'tb_user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name
