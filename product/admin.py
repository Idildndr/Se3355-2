from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Category, Product,ProductImage,SuperCategory

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Set the number of empty forms to display

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(SuperCategory)



