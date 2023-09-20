main

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('raca', models.CharField(max_length=30)),
                ('idade', models.CharField(max_length=8)),
                ('desc', models.CharField(max_length=200)),
                ('obs', models.CharField(max_length=200)),
                ('sexo', models.CharField(max_length=10)),
                ('fk_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pet', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ImagemPet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagem', models.ImageField(upload_to='imgPet/')),
                ('fk_pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imagem_pet', to='pages.pet')),
            ],
        ),
    ]
