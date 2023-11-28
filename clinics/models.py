from django.db import models
from django.core.validators import RegexValidator
from django.conf import settings

#TODO add slug for URL, throw a little about icon up there. Separate w/ '-'s 
class Clinic(models.Model):
    clinicname = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=60) 
    adress = models.CharField(max_length=100)
    adressline2 = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2) #choices=states)
    postcode = models.CharField(max_length=9)
    about = models.TextField(max_length=1500, blank=True)

    TELE_SERVICE = (
        ('Y', 'Yes'),
        ('N', 'No'),
    )

    PAYMENT_TYPE = (
        ('Cash', 'Cash'),
        ('Insurance', 'Insurance'),
        ('Both', 'Both'),
    )

    telehealth = models.CharField(max_length=1, choices=TELE_SERVICE)
    payment = models.CharField(max_length=9, choices=PAYMENT_TYPE)
    created_date = models.DateTimeField(auto_now_add=True)
    last_edit = models.DateTimeField(auto_now=True)
    
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='clinics', on_delete=models.CASCADE) 

    # Users not added to this automatically, duh. 
    # Debug tip, make sure database is migrated to have chance at expected behavior.
    # Set admin perms in create_view.
    practitioners = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='ClinicTeam',
        through_fields=('clinic','practitioner'),
        related_name='jobsites', 
    ) 

    def query_admin(self):
        """ Loads all practitioners with admin privileges"""
        # DON"T NEED THIS. KEEPING ADMIN PRIV IN THROUGH TABLE. WHAT IF USER ISN"T PART OF CLINIC, WHAT WOULD THEY BE AN ADMIN OF.
        pass


    def __str__(self):
        return self.clinicname
    
    class Meta:
        ordering = ['clinicname']


class ClinicTeam(models.Model):
    # Does on delete here mean this table is removed when the user is deleted or do both have to be deleted? 
    # Only allow below perms if they are clinic admin, check for healthcare provider in view. 
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    practitioner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    is_admin = models.BooleanField('Admin', default=False)

    class Meta:
        permissions = [
            ("set_admin_status", "Can assign and revoke the admin status of other team members"),
            ("invite_team_members", "Can invite other team members")
        ]


class InviteStatus(models.Model):
    practitioner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, blank=True) #change to pending.