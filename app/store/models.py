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
    images=models.ImageField(upload_to=category_image_file_path)
    stock=models.IntegerField()
    is_available=models.BooleanField(default=True)
    created_date=models.DateTimeField(auto_now_add=True)
    modified_date=models.DateTimeField( auto_now=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)

    def get_url(self):
        return reverse('product-detail' , args=[self.category.slug , self.slug])

    def __str__(self):
        return self.product_name


