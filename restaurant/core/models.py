from django.db import models

# Create your models here.
class Message(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField()
    