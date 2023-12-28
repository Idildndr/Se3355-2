from django.db import models

class SuperCategory(models.Model):
    name = models.CharField(max_length=140)
    
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=140)  
    parent_category = models.ForeignKey('self', null=True, blank=True, related_name='subcategories', on_delete=models.CASCADE)
    super_category = models.ForeignKey(SuperCategory, null=True, blank=True, related_name='categories', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    superCategory = models.ForeignKey(SuperCategory, null=True, blank=True, related_name='super_categories', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='item_images', blank=True, null=True)
