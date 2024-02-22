from django.contrib import admin
from .models import Products

# Register your models here.
class Productsadmin(admin.ModelAdmin):
    list_display=('image','sname','quantity','price','description')
    fields=['image','sname','quantity','price','description']
admin.site.register(Products,Productsadmin)