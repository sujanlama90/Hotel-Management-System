from django.contrib import admin
from .models import Category,Momo
# Register your models here.
admin.site.register(Category)
@admin.register(Momo)
class MomoAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_available', 'created_at', 'update_at')
    list_filter = ('category', 'is_available')
    search_fields = ('name', 'desc')