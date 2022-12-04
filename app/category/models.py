from django.db import models
from django.urls import reverse
import os
import uuid
# Create your models here.
def category_image_file_path(instance , filename):
    ext=os.path.splitext(filename)[1]
    filename=f'{uuid.uuid4()}{ext}'
    return os.path.join( 'uploads','recipe' , filename)

class Category(models.Model):
    category_name=models.CharField( max_length=255 , unique=True)
    slug=models.SlugField( max_length=255 , unique=True)
    description=models.TextField(blank=True)
    cat_image=models.ImageField(upload_to=category_image_file_path , blank=True)

    def get_url(self):
        return reverse('products-by-category' , args=[self.slug])

    def __str__(self):
        return self.category_name

