from .views import ImageCodeView,SMSCodeView
from django.urls import path,re_path

urlpatterns = [
    re_path(r'^image_codes/(?P<uuid>[\w-]+)/$',ImageCodeView.as_view()),
    re_path(r'^sms_codes/(?P<mobile>1[3-9]\d{9})',SMSCodeView.as_view()),
]
