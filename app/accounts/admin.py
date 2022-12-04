from django.contrib import admin
from accounts.models import User
from django.contrib.auth.admin import UserAdmin as BaseUser
class UserAdmin(BaseUser):
    ordering=['-date_joined']
    list_display=['user_name' , 'email']
    list_display_links=['email']
    fieldsets = (
        (None, {
            "fields": (
                'user_name','email','password'
            ),
        }),
        (
            ('Permissions'), {'fields' : (
                'is_staff','is_active',"is_superuser"
            )}
        ),
        (('Impotant Dtaes') , {'fields':('last_login','date_joined')}),
    )

    readonly_fields=['last_login' , 'date_joined']
    add_fieldsets=(
        (None , {
            'classes':('wide',) ,
            'fields':(
                'name',
                'email',
                'password1',
                'password2',
                'is_active',
                'is_staff',
                'is_superuser'
            ),
        }),
    )
# Register your models here.

admin.site.register(User , UserAdmin)