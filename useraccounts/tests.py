from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Patient, PelvicTherapist


# Python warnings: -Wa flag to display depreciation warnings
class CustomUsersManagersTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email="normal@user.com", password="foo", first_name="Randy")
        self.assertEqual(user.email, "normal@user.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_patient)
        self.assertFalse(user.is_healthcare_provider)
        self.assertFalse(user.is_superuser)
        self.assertEqual(user.first_name, "Randy")
        try:
            self.assertIsNone(user.username)
        except AttributeError:
            pass

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(email="super@user.com", password="foo")
        self.assertEqual(admin_user.email, "super@user.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            self.assertIsNone(admin_user.username)
        except AttributeError: 
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="super@user.com", password="foo", is_superuser=False)
        with self.assertRaises(TypeError):
                User.objects.create_user(password="foobar")
    
    def test_create_patient_profile(self):
            User = get_user_model()
            profile = User.objects.create_user(email="patient@user.com", password="foo", is_patient=True)
            self.assertTrue(profile.is_patient)
            self.assertFalse(profile.is_healthcare_provider)
            self.assertFalse(profile.is_superuser)
            #Testing relationship works via proxy model. 
            newpatient = Patient.objects.get(user_id=profile.id)
            self.assertEqual(newpatient.user_id, profile.id)
            print(f"\n\n\nPatient id: {newpatient.user_id}. CustomUser id: {profile.id}\n")
            with self.assertRaises(TypeError):
                User.objects.create_user(password="foobar", is_patient=True)

    def test_create_pelvic_therapist(self):
            User = get_user_model()
            profile = User.objects.create_user(email="pelvictherapist@user.com", password="foo", is_healthcare_provider=True)
            self.assertTrue(profile.is_healthcare_provider)
            self.assertFalse(profile.is_patient)
            self.assertFalse(profile.is_superuser)
            #Testing relationship works directly via model. 
            newpt = PelvicTherapist.objects.get(user_id=profile.id)
            self.assertEqual(newpt.user_id, profile.id)
            print(f"\n\n\n PelvicTherapist ID: {newpt.user_id}. CustomUser ID: {profile.id}\n")

            # Check fails without email
            with self.assertRaises(TypeError):
                User.objects.create_user(password="foobar", is_pelvic_therapist=True)





    