from django.db import models
from django.contrib.auth.models import  AbstractBaseUser
from .managers import UserManager






class User(AbstractBaseUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        MANAGER = "MANAGER", "Manager"
        USER = "USER", "User"


    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=11,unique=True)
    username = models.CharField(max_length=100,unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    role = models.CharField(max_length=50, choices=Role.choices, default=Role.USER)


    objects = UserManager()

    USERNAME_FIELD = 'phone_number'

    REQUIRED_FIELDS = ['full_name','username']

    def __str__(self):
        return self.phone_number

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


    @property
    def is_staff(self):
        return self.is_admin






