import uuid , os
from django.urls import reverse
from django.db import models
from category.models import Category




def category_image_file_path(instance , filename):
    ext=os.path.splitext(filename)[1]
    filename=f'{uuid.uuid4()}{ext}'
    return os.path.join( 'uploads','products' , filename)
# Create your models here.
class Products(models.Model):
    product_name=models.CharField( max_length=255 , unique=True)
    slug=models.SlugField(max_length=255 , unique=True)
    price=models.IntegerField()
    description=models.TextField(blank=True)
    images=models.ImageField(upload_to=category_image_file_path , blank=True)
    stock=models.IntegerField()
    is_available=models.BooleanField(default=True)
    created_date=models.DateTimeField(auto_now_add=True)
    modified_date=models.DateTimeField( auto_now=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)

    def get_url(self):
        return reverse('product-detail' , args=[self.category.slug , self.slug])

    def __str__(self):
        return self.product_name
var_choices=[
    ('color','color') ,
    ('size' , 'size'),
    ]

class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color' , is_active=True)
    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size' , is_active=True)
class Variation(models.Model):

    product=models.ForeignKey(Products(), on_delete=models.CASCADE)
    variation_category=models.CharField(max_length=100 , choices=var_choices)
    variation_value=models.CharField(max_length=100)
    is_active=models.BooleanField(default=True)

    created_date=models.DateField( auto_now=True, auto_now_add=False)
    objects=VariationManager()

    def __str__(self):
        return self.variation_value



