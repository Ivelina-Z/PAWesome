from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import CharField
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View

from django.views.generic import DetailView, ListView, UpdateView, DeleteView

from PAWesome.adoption.forms import FilledAdoptionForm
from PAWesome.adoption.models import SubmittedAdoptionSurvey
from PAWesome.animal.models import Animal, AdoptedAnimalsArchive, AnimalPhotos, AdoptedAnimalPhotosArchive
from PAWesome.animal.views import BaseAdoptView
from PAWesome.mixins import OrganizationMixin
from PAWesome.organization.forms import OrganizationForm, EmployeeForm
from PAWesome.organization.models import Organization, Employee


# PUBLIC PART

class AllOrganizationsView(ListView):
    model = Organization
    template_name = 'all-organizations.html'


def view_organization(request, slug):
    return render(request, 'organization-details.html')


# PRIVATE PART


class DashboardView(OrganizationMixin, LoginRequiredMixin, DetailView):
    login_url = 'login'
    model = Organization
    template_name = 'dashboard.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        organization = self.get_organization()
        return queryset.filter(slug=organization.slug)


class AllAnimalsView(OrganizationMixin, LoginRequiredMixin, BaseAdoptView):
    login_url = 'login'

    def get_queryset(self):
        queryset = super().get_queryset()
        organization = self.get_organization()
        return queryset.filter(organization=organization.pk).prefetch_related('animalphotos_set')


class PendingAdoptForms(OrganizationMixin, LoginRequiredMixin, ListView):
    login_url = 'login'
    template_name = 'waiting-for-approval.html'
    model = SubmittedAdoptionSurvey

    def get_queryset(self):
        queryset = super().get_queryset()
        organization = self.get_organization()
        return queryset.filter(organization=organization.pk)


class HandleAdoptionForm(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = ['animal.add_adoptedanimalsarchive']
    login_url = 'login'
    form_class = FilledAdoptionForm

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            return super().dispatch(request, *args, **kwargs)
        return self.get(request, *args, **kwargs)

    def get_form(self, request):
        form = self.form_class(request)
        json_data = SubmittedAdoptionSurvey.objects.get(pk=self.kwargs['pk']).questionnaire_text
        # except:
        for field_name, field_value in json_data.items():
            form.fields[field_name] = CharField(initial=field_value, disabled=True)
        return form

    def get(self, request, *args, **kwargs):
        form = self.get_form(request.GET)
        return render(request, 'waiting-for-approval-details.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.get_form(request.POST)
        if form.is_valid():
            action = request.POST.get('action')
            questionnaire = SubmittedAdoptionSurvey.objects.get(pk=self.kwargs['pk'])
            if action == 'adopt':
                # try:
                animal = questionnaire.animal
                photos = AnimalPhotos.objects.filter(animal=animal.pk)
                animal_data = animal.__dict__.copy()
                [animal_data.pop(key) for key in ('_state', 'id')]
                # except:
                archived_animal = AdoptedAnimalsArchive.objects.create(filled_questionnaire_text=form.cleaned_data,
                                                                       **animal_data)

                for photo in photos:
                    photo_data = photo.__dict__.copy()
                    [photo_data.pop(key) for key in ('_state', 'id')]
                    photo_instance = AdoptedAnimalPhotosArchive(**photo_data)
                    photo_instance.animal = archived_animal
                    photo_instance.save()
                    AnimalPhotos.delete(photo)

                Animal.delete(animal)
            elif action == 'reject':
                # try:
                questionnaire.delete(delete_by_reject=True)
                # except:

            return redirect(reverse_lazy('dashboard', kwargs={'slug': request.user.organization.slug}))
        return render(request, 'waiting-for-approval-details.html', {'form': form})


class ViewProfile(OrganizationMixin, LoginRequiredMixin, DetailView):
    login_url = 'login'
    template_name = 'view-profile.html'

    def get_object(self, queryset=None):
        model = None
        if self.is_organization():
            model = Organization
        elif self.is_employee():
            model = Employee

        # try:
        obj = model.objects.get(pk=self.kwargs['pk'])
        # except:
        return obj


class EditProfile(OrganizationMixin, LoginRequiredMixin, UpdateView):
    login_url = 'login'
    template_name = 'profile-edit.html'

    def get_object(self, queryset=None):
        if self.is_organization():
            model = Organization
        elif self.is_employee():
            model = Employee
        else:
            model = None
        obj = model.objects.get(pk=self.kwargs['pk'])
        return obj

    def get_form_class(self):
        if self.is_organization():
            form_class = OrganizationForm
        elif self.is_employee():
            form_class = EmployeeForm
        else:
            form_class = None
        return form_class

    def get_success_url(self):
        return reverse_lazy('dashboard', kwargs={'slug': self.get_organization().slug})


class DeleteProfile(OrganizationMixin, DeleteView):
    template_name = 'profile-delete.html'
    success_url = reverse_lazy('homepage')

    def get_object(self, queryset=None):
        if self.is_organization():
            model = Organization
        elif self.is_employee():
            model = Employee
        else:
            model = None
        # try:
        obj = model.objects.get(pk=self.kwargs['pk'])
        # except:
        #     pass
        return obj
