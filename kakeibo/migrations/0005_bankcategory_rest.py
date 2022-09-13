# Generated by Django 3.2.15 on 2022-09-13 15:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kakeibo', '0004_delete_rest'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='カテゴリ名')),
            ],
        ),
        migrations.CreateModel(
            name='Rest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rest', models.IntegerField(verbose_name='残り金額')),
                ('date', models.DateField(verbose_name='日付')),
                ('bank_category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='kakeibo.bankcategory', verbose_name='銀行')),
            ],
        ),
    ]
