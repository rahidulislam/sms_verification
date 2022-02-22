from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,PermissionsMixin
from django.utils.translation import gettext_lazy
import pyotp
# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("User must have email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True")
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(verbose_name="Email Address", max_length=255, unique=True)
    key = models.CharField(max_length=100, unique=True, blank=True)
    is_staff = models.BooleanField(gettext_lazy('Staff status'), default=False)
    is_superuser = models.BooleanField(gettext_lazy('Superuser status'), default=False)
    is_active = models.BooleanField(gettext_lazy('Active'), default=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'

    def get_full_name(self):
        return self.email


    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    def authenticate(self, otp):
        """This method authenticate given otp"""
        provided_otp = 0
        try:
            provided_otp = int(otp)
        except:
            return False
        # Here is Time based OTP. otp must be provided within 300 seconds
        t=pyotp.TOTP(self.key, interval=300)
        return t.verify(provided_otp)
        

    
    