from django.contrib import admin
from .models import Category, Product
# Register your models here.


# admin.site.register(Category)
# admin.site.register(Product)
@admin.register(Category)
class Categor1yAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title',)}