from django.urls import path,re_path
from . import views
urlpatterns = [
    path(r'carts',views.CartsView.as_view(),name='info'),
    path(r'carts/selection/', views.CartsSelectAllView.as_view()),
    path(r'carts/simple/',views.CartsSimpleView.as_view())

]