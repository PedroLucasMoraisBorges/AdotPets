from django.db import models
from auth_user.models import Company

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=150)
    desc = models.CharField(max_length=250)
    value = models.CharField(max_length=6, default= 0)
    fk_company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='product')
    category = models.CharField(max_length=50, null=False)