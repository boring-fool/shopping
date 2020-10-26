from django.urls import path
from . import views
urlpatterns = [
    path(r'orders/settlement/',views.OrderSettlementView.as_view(),name='settlement'),
    path(r'orders/commit/',views.OrderCommitView.as_view()),
    path(r'orders/success/', views.OrderSuccessView.as_view()),
]