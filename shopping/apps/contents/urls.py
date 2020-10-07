from django.urls import path,include
from .views import IndexView
urlpatterns = [
    path(r'',IndexView.as_view(),name='index'),
]