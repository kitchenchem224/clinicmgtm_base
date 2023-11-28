from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import datetime
from django.core.validators import RegexValidator
from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager 

"""
11/4 Purged database
"""
class CustomUser(AbstractUser):
    """Base user for all extended classes"""
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    email = models.EmailField(_('email address'), unique=True) 
    email_verified = models.BooleanField('email verified', default=False) 
    is_patient = models.BooleanField('Patient', default=False)
    is_healthcare_provider = models.BooleanField('Healthcare Provider', default=False)

    objects = CustomUserManager()

    def __str__(self):
        if self.first_name:
            return self.first_name + ': ' + self.email
        return self.email
    

class PatientProfile(models.Model):
    """Model for patient specific information"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    postcode = models.IntegerField(validators=[RegexValidator(r'^\d{5}([ \-]\d{4})?')],blank=True, null=True) 
    age = models.IntegerField(validators=[RegexValidator('^[0-9]{2}$')], blank=True, null=True)
 
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('NA', 'Decline To Say'),
    )

    gender = models.CharField(max_length=2, choices=GENDER_CHOICES, blank=True, null=True)

    created_date = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    def was_created_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.created_date <= now
    
    def __str__(self):
        return self.user.email
    
class Patient(PatientProfile):
    """Patient Proxy Model"""
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(CustomUser.is_patient == True)

    class Meta:
        proxy = True


class HealthcareProvider(models.Model):
    """Healthcare user parent class, each type has subclass of HealthcareProvider
    Cannot add proxy models to abstract models"""
    first_name = models.CharField(max_length=60, default='foo')
    last_name = models.CharField(max_length=60, default='bar') 

    is_clinic_admin = models.BooleanField('clinic admin', default=False)

    GENDER_SPECIALTY = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('NA', 'Any/Not Applicable'),
    )
    gender_specialty = models.CharField(max_length=2, choices=GENDER_SPECIALTY)

    GYNECOLOGIST = 1
    PELVIC_THERAPIST = 2
    PROCTOLOGIST = 3
    UROLOGIST = 4
    
    HEALTHCARE_SPECIALTY = (
        (GYNECOLOGIST, 'Gynecologist'),
        (PELVIC_THERAPIST, 'Pelvic Therapist'),
        (PROCTOLOGIST, 'Proctologist'),
        (UROLOGIST, 'Urologist'),
    )
 
    provider_specialty = models.SmallIntegerField(choices=HEALTHCARE_SPECIALTY, null=True)
    about = models.TextField(max_length=1000, blank=True, null=True)

    created_date = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True    


class PelvicTherapistManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(CustomUser.is_healthcare_provider == True) # Edit to access type - make my life easier

class PelvicTherapist(HealthcareProvider):
    """Model for Pelvic Therapist Specific Information"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    CERTIFICATION_CHOICES = (
        ('a', 'example'),
        ('b', 'example2'),
    )

    certifications = models.CharField(max_length=1, choices=CERTIFICATION_CHOICES, null=True)

    def __str__(self):
        return self.user.email


class PelvicTherapistProxy(PelvicTherapist): #Useless
    """Pelvic Therapist Proxy Model"""
    PelvicTherapist = PelvicTherapistManager()

    class Meta:
        proxy = True
        


"""TODO Edit the below to fit with specialty specific requirements. Need to know more about these before I am able to do really anything. """
class Gynecologist(HealthcareProvider):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    CERTIFICATION_CHOICES = (
        ('a', 'example'),
        ('b', 'example2'),
    )

    certifications = models.CharField(max_length=1, choices=CERTIFICATION_CHOICES, null=True)

    def __str__(self):
        return self.user.email
    

class Proctologist(HealthcareProvider):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    CERTIFICATION_CHOICES = (
        ('a', 'example'),
        ('b', 'example2'),
    )

    certifications = models.CharField(max_length=1, choices=CERTIFICATION_CHOICES, null=True)

    def __str__(self):
        return self.user.email
    

class Urologist(HealthcareProvider):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    CERTIFICATION_CHOICES = (
        ('a', 'example'),
        ('b', 'example2'),
    )

    certifications = models.CharField(max_length=1, choices=CERTIFICATION_CHOICES, null=True)

    def __str__(self):
        return self.user.email