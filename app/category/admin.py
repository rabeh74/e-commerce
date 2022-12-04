from django.contrib import admin
from category.models import Category
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('category_name',)}
# Register your models here.
admin.site.register(Category , CategoryAdmin)