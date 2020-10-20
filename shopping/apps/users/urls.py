from . import views
from django.urls import path,re_path

urlpatterns = [
    path(r'register',views.RegisterView.as_view(),name='register'),
    path(r'logout',views.LogoutView.as_view(),name='logout'),
    path(r'info',views.UserInfoView.as_view(),name='info'),
    path(r'emails',views.EmailView.as_view()),
    path(r'address',views.AddressView.as_view(),name='address'),
    path(r'password',views.PasswordView.as_view(),name='password'),
    path(r'browse_histories',views.UserBrowseHistory.as_view()),
    re_path(r'^addresses/create/', views.AddressCreateView.as_view()),
    re_path(r'^addresses/(?P<address_id>\d+)/$', views.UpdateDestoryAddressView.as_view()),
    re_path(r'^addresses/(?P<address_id>\d+)/default/$', views.DefaultAddressView.as_view()),
    re_path(r'^addresses/(?P<address_id>\d+)/title/$', views.UpdateTitleAddressView.as_view()),
    re_path(r'^emails/verification/',views.VerifyEmailView.as_view()),
    re_path(r'^login',views.LoginView.as_view(),name='login'),
    re_path(r'^usernames/(?P<username>[a-zA-Z0-9_-]{5,20})/count/$',views.UsernameCountView.as_view()),
    re_path(r'mobiles/(?P<mobile>[\d]+)/count/$',views.MobileCountView.as_view()),
]
