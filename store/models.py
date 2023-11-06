from django.db import models
from auth_user.models import Company

from django.contrib.auth.models import User


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=150)
    desc = models.CharField(max_length=250)
    value = models.FloatField()
    fk_company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='product')
    category = models.CharField(max_length=50, null=False)
    discount = models.FloatField(null=True, blank=True)

class ProductImage(models.Model):
    fk_product = models.ForeignKey(Product, related_name='image', on_delete=models.CASCADE)
    img = models.ImageField(upload_to='product_image')

