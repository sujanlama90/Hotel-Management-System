from django.db import models

# Create your models here.
class Message(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField()

class Category(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='categoryImages',null=True)

    def __str__(self):
        return self.title

class Momo(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name='items')
    desc = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='momoImage')
    is_available = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

class Review(models.Model):
    name = models.CharField(max_length=200)
    message = models.TextField()
    order = models.CharField(max_length=200)
    rating =models.PositiveSmallIntegerField()