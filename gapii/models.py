from django.db import models

# Create your models here.
class Person(models.Model):
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=12)
    address = models.CharField(max_length=120)
    website=models.CharField(max_length=100)
    img = models.ImageField(upload_to='images/',null=True)
