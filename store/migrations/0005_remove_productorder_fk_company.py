# Generated by Django 4.2.7 on 2023-11-08 11:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_productorder_orderiten'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productorder',
            name='fk_company',
        ),
    ]
