# Generated by Django 4.2.7 on 2023-11-08 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_orderiten_fk_address_orderiten_fk_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='divided',
            field=models.IntegerField(default=0),
        ),
    ]
