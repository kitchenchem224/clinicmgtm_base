from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import HealthcareProvider, PelvicTherapistProxy, CustomUser, Gynecologist, Proctologist, Urologist
from django.db import models
from django.db import transaction

class PatientProfileSignupForm(UserCreationForm):
    """Sends signal connect profile, initial value are null
        Replaces the two forms one template approach"""
    class Meta(UserCreationForm.Meta):  
        model = CustomUser
        fields = ('email',)
   
    def save(self): 
        data = super().save(commit=False) 
        data.is_patient = True
        data.save() 
        return data
    

class ProviderProfileSignupForm(UserCreationForm):
    """Inherits user creation form to handle authentication email + password"""
    first_name = forms.CharField(max_length=60) 
    last_name = forms.CharField(max_length=60)
    provider_specialty = forms.ChoiceField(choices=HealthcareProvider.HEALTHCARE_SPECIALTY)
    gender_specialty = forms.ChoiceField(choices=HealthcareProvider.GENDER_SPECIALTY)
    about = models.TextField(max_length=1000, blank=True)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email',)
       
    @transaction.atomic
    def save(self): 
        data = super().save(commit=False) 
        data.is_healthcare_provider = True
        data.save()
        # TODO refactor to swtich.
        # Reverse lookup
        if data.provider_specialty == 1:
            modeltype = Gynecologist
        elif data.provider_specialty == 2:
            modeltype = PelvicTherapistProxy
        elif data.provider_specialty == 3:
            modeltype = Proctologist
        else: 
            modeltype = Urologist

        modeltype.objects.create( #No reason for this proxy
            user=data,
            first_name=self.cleaned_data.get('first_name'),
            last_name=self.cleaned_data.get('last_name'),
            gender_specialty=self.cleaned_data.get('gender_specialty'),
            provider_specialty=self.cleaned_data.get('provider_specialty'),
        )    
        return data
    