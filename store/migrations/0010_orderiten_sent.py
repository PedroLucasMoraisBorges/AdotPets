# Generated by Django 4.2.7 on 2023-11-10 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_alter_product_divided'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderiten',
            name='sent',
            field=models.BooleanField(default=False),
        ),
    ]
