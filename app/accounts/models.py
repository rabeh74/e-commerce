from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self,user_name ,first_name,last_name,email,password=None , **kwargs):
        if not email:
            raise ValueError('should enter email :')
        if not user_name:
            raise ValueError(' should enter username')


        user=self.model(
            email=self.normalize_email(email),user_name=user_name,
            last_name=last_name,
            first_name=first_name,
            )
        user.set_password(password)
        user.save(using=self._db)

        return user
    def create_superuser(self ,user_name, email,password=None , **kwargs):
        if not email:
            raise ValueError('should enter email :')
        if not user_name:
            raise ValueError(' should enter username')


        user=self.model(
            user_name=user_name,
            email=self.normalize_email(email),
            **kwargs
            )
        user.set_password(password)
        user.is_admin=True
        user.is_staff=True
        user.is_active=True
        user.is_superuser=True

        user.save(using=self._db)

        return user




class User(AbstractBaseUser , PermissionsMixin):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    user_name=models.CharField(max_length=50 , unique=True)
    phone_number=models.CharField(max_length=50 ,)
    email=models.EmailField(max_length=254 , unique=True)

    date_joined=models.DateTimeField(auto_now_add=True)
    last_login=models.DateTimeField(auto_now_add=True)
    is_admin=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_active=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['first_name' , 'last_name' , 'user_name']
    objects=UserManager()
    def __str__(self):
        return self.email

    def has_perm(self , perm , obj=None):
        return self.is_admin

    def has_module_perms(self,add_label):
        return True
