# Generated by Django 3.2.15 on 2022-09-13 15:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kakeibo', '0003_alter_paymentcategory_name'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Rest',
        ),
    ]