# What are these: 
# from django.contrib.auth import REDIRECT_FIELD_NAME
# from django.contrib.auth.decorators import user_passes_test
from .models import Patient, CustomUser
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=CustomUser) # could also add this as a method inside the model class
def create_user_type(sender, instance, created, **kwargs):
    """Create appropriate extended customS user instance on signup"""
    if created and instance.is_patient == True:
        Patient.objects.create(user=instance)

