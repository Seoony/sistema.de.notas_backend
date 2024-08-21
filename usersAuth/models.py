from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, email, nombres, apellido_pat, apellido_mat,
                    dni, password=None):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(
          email=email,
          nombres=nombres,
          apellido_pat=apellido_pat,
          apellido_mat=apellido_mat,
          dni = dni
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, nombres, apellido_pat,
                        apellido_mat, dni, password=None):
        user = self.create_user(email, nombres, apellido_pat,
                                apellido_mat, dni, password)
        user.is_admin = True
        user.is_staff = True
        user.save()
        return user
      
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=125)
    dni = models.CharField(max_length=8, unique=True)
    nombres = models.CharField(max_length=63)
    apellido_pat = models.CharField(max_length=31)
    apellido_mat = models.CharField(max_length=31)
    fecha_nac = models.DateField(blank=True, null=True)
    celular = models.CharField(max_length=9, blank=True, null=True)
    est_reg = models.CharField(max_length=1, default='A')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombres', 'apellido_pat', 'apellido_mat'
                       , 'dni']
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.nombres.split(" ")[0] + ' ' + self.apellido_pat