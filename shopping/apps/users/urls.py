from .views import RegisterView,UsernameCountView,MobileCountView
from django.urls import path,re_path

urlpatterns = [
    path(r'register',RegisterView.as_view(),name='register'),
    re_path(r'^usernames/(?P<username>[a-zA-Z0-9_-]{5,20})/count/$',UsernameCountView.as_view()),
    re_path(r'mobiles/(?P<mobile>[\d]+)/count/$',MobileCountView.as_view()),
]
