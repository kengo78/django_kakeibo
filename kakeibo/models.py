from django.db import models
from django.utils import timezone

class PaymentCategory(models.Model):#支払いのカテゴリ
    name = models.CharField('カテゴリ名', max_length=16)

    def __str__(self):
        return self.name
    
class Payment(models.Model):#支払額
    date = models.DateField('日付')
    price = models.IntegerField('金額')
    category = models.ForeignKey(PaymentCategory, on_delete=models.PROTECT, verbose_name='カテゴリ')
    description = models.TextField('概要', null=True, blank=True)


class IncomeCategory(models.Model):
    name = models.CharField('カテゴリ名', max_length=32)

    def __str__(self):
        return self.name


class Income(models.Model):
    date = models.DateField('日付')
    price = models.IntegerField('金額')
    category = models.ForeignKey(IncomeCategory, on_delete=models.PROTECT, verbose_name='カテゴリ')
    description = models.TextField('概要', null=True, blank=True)
    
class BankCategory(models.Model):
    name = models.CharField('カテゴリ名', max_length=32)

    def __str__(self):
        return self.name

class Rest(models.Model):
    date = models.DateField('日付',default=timezone.now)
    rest = models.IntegerField('金額')
    category = models.ForeignKey(BankCategory, on_delete=models.PROTECT,verbose_name='銀行')
    