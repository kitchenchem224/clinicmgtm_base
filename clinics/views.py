from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView
from django.views import View
from .models import Clinic, ClinicTeam, InviteStatus
from .forms import ClinicTeamAddForm, LocationCreateForm, LocationUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from accounts.models import CustomUser
from django.contrib.auth.models import Group


class LocationCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = "locations.add_clinic" 
    model = Clinic
    form_class = LocationCreateForm
    template_name = 'locations/create_location.html'

    def form_valid(self, form):
        user = self.request.user
        location = form.save(commit=False)
        location.created_by = user
        location.save()
        #Creating Clinic team directly here. 
        team = ClinicTeam.objects.create(
           clinic=location,
           practitioner=user,
           is_admin=True)
        
        team.save()
        # Give user clinic admin permissions. Default on clinic creation
        permission_group = Group.objects.get(name="Clinic Administrator")
        user.groups.add(permission_group)

        return render(self.request, "accounts/userdash.html", {user: user}) 
    
class LocationDetailView(DetailView):
    model = Clinic
    template_name='locations/detail_location.html'

# TODO Invite only once. 
class LocationUpdateView(UserPassesTestMixin, PermissionRequiredMixin, UpdateView):
    permission_required = "locations.change_clinic"
    model = Clinic
    form_class = LocationUpdateForm
    template_name = 'locations/update_location.html'
    def test_func(self):
        clinic = get_object_or_404(Clinic, pk=self.kwargs.get('pk'))
        user = self.request.user
        #Check if user has is in all pracitioners and if they have admin privs. 
        if user in clinic.practitioners.all(): 
            if clinic.practitioners.filter(id=user.id, clinicteam__is_admin=True): 
                return True
            return False
    def get_success_url(self):
        return reverse('locations:test')

class ClinicTeamManagementView(UserPassesTestMixin, PermissionRequiredMixin, View):
    permission_required = ("locations.set_admin_status", "locations.invite_team_members")
    _clinic = None 
    def test_func(self):
        self._clinic = get_object_or_404(Clinic, pk=self.kwargs.get('pk'))
        user = self.request.user
        if self._clinic.practitioners.filter(id=user.id, clinicteam__is_admin=True):
            return True
        return False

    def get(self, request, **kwargs):
        form = ClinicTeamAddForm()
        return render(request, 'locations/invite.html', {"form": form, "clinic":self._clinic}) #Why is this needed.
    
    def post(self, request, **kwargs):
        form = ClinicTeamAddForm(request.POST)
        if form.is_valid():
            print(self._clinic)
            recipient = form.cleaned_data["recipient"]
            message = form.cleaned_data["message"] 
            admin_perm = form.cleaned_data["admin_perm"]

            try:
                clinician = CustomUser.objects.get(email=recipient)
                ClinicTeam.objects.create(clinic=self._clinic, practitioner=clinician, is_admin=admin_perm)  
                InviteStatus.objects.create(practitioner=clinician, status="false")
                # InviteStatus.objects.create(practitioner=clinician, invite_accepted=False)
                    # TODO status to pending                    

            except CustomUser.DoesNotExist:
                #TODO implement
                print("success")                
            
            return HttpResponse(f"SENT {recipient} and {message} and {self.request}")
        return HttpResponse(f"Form failed {self.request}")
    

class LocationDeleteView(UserPassesTestMixin, PermissionRequiredMixin, DeleteView)