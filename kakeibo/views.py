#kakeibo/views.py
from django.views import generic
from .models import Payment, PaymentCategory, Income, IncomeCategory
from django.urls import reverse_lazy

from .forms import PaymentSearchForm, IncomeSearchForm,PaymentCreateForm, IncomeCreateForm 
from django.contrib import messages 
from django.shortcuts import redirect 

import numpy as np
import pandas as pd
from django_pandas.io import read_frame
from .plugin_plotly import GraphGenerator


class PaymentList(generic.ListView):
    template_name = 'kakeibo/payment_list.html'
    model = Payment
    ordering = '-date'
    paginate_by = 5

    # 追加
    def get_queryset(self):
        queryset = super().get_queryset()
        self.form = form = PaymentSearchForm(self.request.GET or None)

        if form.is_valid():
            year = form.cleaned_data.get('year')
            # 何も選択されていないときは0の文字列が入るため、除外
            if year and year != '0':
                queryset = queryset.filter(date__year=year)

            # 何も選択されていないときは0の文字列が入るため、除外
            month = form.cleaned_data.get('month')
            if month and month != '0':
                queryset = queryset.filter(date__month=month)

            # 〇〇円以上の絞り込み
            greater_than = form.cleaned_data.get('greater_than')
            if greater_than:
                queryset = queryset.filter(price__gte=greater_than)
            
            # 〇〇円以下の絞り込み
            less_than = form.cleaned_data.get('less_than')
            if less_than:
                queryset = queryset.filter(price__lte=less_than)
            
            # キーワードの絞り込み
            key_word = form.cleaned_data.get('key_word')
            if key_word:
                # 空欄で区切り、順番に絞る、and検索
                if key_word:
                    for word in key_word.split():
                        queryset = queryset.filter(description__icontains=word)
            
            # カテゴリでの絞り込み
            category = form.cleaned_data.get('category')
            if category:
                queryset = queryset.filter(category=category)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # search formを渡す
        context['search_form'] = self.form

        return context
    
class IncomeList(generic.ListView):
    template_name = 'kakeibo/income_list.html'
    model = Income
    ordering = '-date'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.form = form = IncomeSearchForm(self.request.GET or None)

        if form.is_valid():
            year = form.cleaned_data.get('year')
            if year and year != '0':
                queryset = queryset.filter(date__year=year)

            month = form.cleaned_data.get('month')
            if month and month != '0':
                queryset = queryset.filter(date__month=month)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = self.form

        return context
    
class PaymentCreate(generic.CreateView):
    """支出登録"""
    template_name = 'kakeibo/register.html'
    model = Payment
    form_class = PaymentCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '支出登録'
        return context

    def get_success_url(self):
        return reverse_lazy('kakeibo:payment_list')

    # 追加
    # バリデーション時にメッセージを保存
    def form_valid(self, form):
        self.object = payment = form.save()
        messages.info(self.request,
                      f'支出を登録しました\n'
                      f'日付:{payment.date}\n'
                      f'カテゴリ:{payment.category}\n'
                      f'金額:{payment.price}円')
        return redirect(self.get_success_url())
class IncomeCreate(generic.CreateView):
    """収入登録"""
    template_name = 'kakeibo/register.html'
    model = Income
    form_class = IncomeCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '収入登録'
        return context

    def get_success_url(self):
        return reverse_lazy('kakeibo:income_list')
    
    def form_valid(self, form):
        self.object = income = form.save()
        messages.info(self.request,
                      f'収入を登録しました\n'
                      f'日付:{income.date}\n'
                      f'カテゴリ:{income.category}\n'
                      f'金額:{income.price}円')
        return redirect(self.get_success_url())
    
class PaymentUpdate(generic.UpdateView):
    """支出更新"""
    template_name = 'kakeibo/register.html'
    model = Payment
    form_class = PaymentCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '支出更新'
        return context

    def get_success_url(self):
        return reverse_lazy('kakeibo:payment_list')

    def form_valid(self, form):
        self.object = payment = form.save()
        messages.info(self.request,
                      f'支出を更新しました\n'
                      f'日付:{payment.date}\n'
                      f'カテゴリ:{payment.category}\n'
                      f'金額:{payment.price}円')
        return redirect(self.get_success_url())


class IncomeUpdate(generic.UpdateView):
    """収入更新"""
    template_name = 'kakeibo/register.html'
    model = Income
    form_class = IncomeCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '収入更新'
        return context

    def get_success_url(self):
        return reverse_lazy('kakeibo:income_list')

    def form_valid(self, form):
        self.object = income = form.save()
        messages.info(self.request,
                      f'収入を更新しました\n'
                      f'日付:{income.date}\n'
                      f'カテゴリ:{income.category}\n'
                      f'金額:{income.price}円')
        return redirect(self.get_success_url())


class PaymentDelete(generic.DeleteView):
    """支出削除"""
    template_name = 'kakeibo/delete.html'
    model = Payment

    def get_success_url(self):
        return reverse_lazy('kakeibo:payment_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '支出削除確認'

        return context

    def delete(self, request, *args, **kwargs):
        self.object = payment = self.get_object()

        payment.delete()
        messages.info(self.request,
                      f'支出を削除しました\n'
                      f'日付:{payment.date}\n'
                      f'カテゴリ:{payment.category}\n'
                      f'金額:{payment.price}円')
        return redirect(self.get_success_url())


class IncomeDelete(generic.DeleteView):
    """収入削除"""
    template_name = 'kakeibo/delete.html'
    model = Income

    def get_success_url(self):
        return reverse_lazy('kakeibo:income_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '収入削除確認'

        return context

    def delete(self, request, *args, **kwargs):
        self.object = income = self.get_object()
        income.delete()
        messages.info(self.request,
                      f'収入を削除しました\n'
                      f'日付:{income.date}\n'
                      f'カテゴリ:{income.category}\n'
                      f'金額:{income.price}円')
        return redirect(self.get_success_url())
    
class MonthDashboard(generic.TemplateView):
    """月間支出ダッシュボード"""
    template_name = 'kakeibo/month_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ...
        context['next_month'] = next_month
        
        # ここから追加
        # paymentモデルをdfにする
        queryset = Payment.objects.filter(date__year=year)
        queryset = queryset.filter(date__month=month)
        # クエリセットが何もない時はcontextを返す
        # 後の工程でエラーになるため
        if not queryset:
            return context
        #データフレーム化
        df = read_frame(queryset,
                        fieldnames=['date', 'price', 'category'])

        # グラフ作成クラスをインスタンス化
        gen = GraphGenerator()

        # pieチャートの素材を作成
        df_pie = pd.pivot_table(df, index='category', values='price', aggfunc=np.sum)
        pie_labels = list(df_pie.index.values)
        pie_values = [val[0] for val in df_pie.values]
        plot_pie = gen.month_pie(labels=pie_labels, values=pie_values)
        context['plot_pie'] = plot_pie

        # テーブルでのカテゴリと金額の表示用。
        # {カテゴリ:金額,カテゴリ:金額…}の辞書を作る
        context['table_set'] = df_pie.to_dict()['price']

        # totalの数字を計算して渡す
        context['total_payment'] = df['price'].sum()

        # 日別の棒グラフの素材を渡す
        df_bar = pd.pivot_table(df, index='date', values='price', aggfunc=np.sum)
        dates = list(df_bar.index.values)
        heights = [val[0] for val in df_bar.values]
        plot_bar = gen.month_daily_bar(x_list=dates, y_list=heights)
        context['plot_bar'] = plot_bar

        return context