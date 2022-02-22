from django.db.models.signals import pre_save
from django.dispatch import receiver
from accounts.models import CustomUser
import pyotp



def generate_key():
    """User OTP Key generator"""
    key = pyotp.random_base32()
    if is_unique(key):
        return key
    generate_key()

def is_unique(key):
    try:
        CustomUser.objects.get(key=key)
    except CustomUser.DoesNotExist:
        return True
    return False
    
@receiver(pre_save, sender=CustomUser)
def create_key(sender, instance, **kwargs):
    """This is generated for who do not have keys"""
    if not instance.key:
        instance.key = generate_key()
