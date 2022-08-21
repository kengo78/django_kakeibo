from django.urls import path
from . import views

app_name = 'kakeibo'

urlpatterns = [
    path('', views.PaymentList.as_view(), name='payment_list'),
]