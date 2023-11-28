from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Clinic 


class LocationCreateTestCase(TestCase):
            
       def test_create_clinic(self):
            User = get_user_model()
            profile = User.objects.create_user(email="patient@user.com", password="foo", is_healthcare_provider=True)
            self.assertFalse(profile.is_patient)
            self.assertTrue(profile.is_healthcare_provider)
            self.assertFalse(profile.is_superuser)


            newclinic = Clinic.objects.create(
                 clinicname='testclinic', email='testemail@email.com',
                 adress='123 test st', adressline2='unit123', city='NYC',
                 state='NY', postcode='10021', about='lorisibsum', 
                 telehealth='Yes', payment='Cash', created_by=profile,
            )


            self.assertEqual(newclinic.created_by.id, profile.id)
            print(1)

            with self.assertRaises(TypeError):
                 Clinic.objects.create(password="foobar", is_patient=True)

              #Next figure out the table showing clinic team. And add the logic for that
        
       def test_create_clinic_team(self):
             pass


class LocationUpdateTestCase(TestCase):
      def test_update_clinic(self):
          pass
          # check information no longer old information
          # Check credits associated with the proper user. 


class ClinicTeamManagementTestCase(TestCase):
      pass
      # Check user has perms 
      # Check updates setup
      # Check emails sent 
      