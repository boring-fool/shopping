"""shopping URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^search/', include('haystack.urls')),
    #用户
    path(r'',include(('users.urls','users'),namespace='users')),
    #首页
    path(r'',include(('contents.urls','contents'),namespace='contents')),
    #验证
    path(r'',include(('verifications.urls','verifications'),namespace='verifications')),
    #省份
    path(r'',include(('areas.urls','areas'),namespace='areas')),
    #商品
    path(r'',include(('goods.urls','goods'),namespace='goods')),
    #购物车
    path(r'',include(('carts.urls','carts'),namespace='carts')),
    #订单
    path(r'',include(('orders.urls','orders'),namespace='orders')),
    #支付
    path(r'',include(('payment.urls','payment'),namespace='payment')),
]
