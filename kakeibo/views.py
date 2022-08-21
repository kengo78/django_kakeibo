#kakeibo/views.py
from django.views import generic
from .models import Payment, PaymentCategory, Income, IncomeCategory


class PaymentList(generic.ListView):
    template_name = 'kakeibo/payment_list.html'
    model = Payment
    ordering = '-date'