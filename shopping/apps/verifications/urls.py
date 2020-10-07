from .views import ImageCodeView
from django.urls import path,re_path

urlpatterns = [
    re_path(r'^image_codes/(?P<uuid>[\w-]+)/$',ImageCodeView.as_view()),
]
