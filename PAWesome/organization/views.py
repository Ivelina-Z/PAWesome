from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.forms import CharField, EmailField, EmailInput
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View

from django.views.generic import DetailView, ListView, UpdateView, DeleteView, TemplateView
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import RegionalPhoneNumberWidget

from PAWesome.adoption.forms import FilledAdoptionForm
from PAWesome.adoption.models import SubmittedAdoptionSurvey
from PAWesome.animal.models import Animal, AdoptedAnimalsArchive, AnimalPhotos, AdoptedAnimalPhotosArchive
from PAWesome.animal.views import BaseAdoptView
from PAWesome.mixins import OrganizationMixin
from PAWesome.organization.forms import OrganizationForm, EmployeeForm
from PAWesome.organization.models import Organization, Employee
from PAWesome.organization.plots import dashboard_plots_context


# PUBLIC PART

class AllOrganizationsView(ListView):
    model = Organization
    template_name = 'all-organizations.html'


class ViewOrganization(DetailView):
    model = Organization
    template_name = 'organization-details.html'


# PRIVATE PART

class DashboardView(OrganizationMixin, LoginRequiredMixin, TemplateView):
    login_url = 'login'
    model = Organization
    template_name = 'dashboard.html'

    def get_context_data(self, slug):
        organization = self.get_organization()
        context = super().get_context_data()
        context.update(dashboard_plots_context(organization))
        return context


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


class HandleAdoptionForm(LoginRequiredMixin, View):
    login_url = 'login'
    form_class = FilledAdoptionForm

    # def dispatch(self, request, *args, **kwargs):
    #     if request.method == 'POST':
    #         return super().dispatch(request, *args, **kwargs)
    #     return self.get(request, *args, **kwargs)

    def _get_form(self, request, obj):
        form = self.form_class(request)
        # form.fields['email'].initial = obj.email
        # form.fields['phone_number'].initial = obj.phone_number
        for question, answer in obj.questionnaire_text.items():
            form.fields[question] = CharField(initial=answer, disabled=True)
            form.fields[question].widget.attrs['class'] = 'form-control'
        form.fields['email'] = EmailField(
            initial=obj.email,
            disabled=True,
            widget=EmailInput(attrs={'class': 'form-control'})
        )
        form.fields['phone_number'] = PhoneNumberField(
            initial=obj.phone_number,
            disabled=True,
            widget=RegionalPhoneNumberWidget(attrs={'class': 'form-control'}))
        return form

    def get(self, request, *args, **kwargs):
        submitted_adoption_form = SubmittedAdoptionSurvey.objects.get(pk=self.kwargs['pk'])
        form = self._get_form(request.GET, submitted_adoption_form)
        return render(request, 'waiting-for-approval-details.html', {'form': form})

    def post(self, request, *args, **kwargs):
        if request.user.has_perm('animal.add_adoptedanimalsarchive'):
            submitted_adoption_form = SubmittedAdoptionSurvey.objects.get(pk=self.kwargs['pk'])
            form = self._get_form(request.POST, submitted_adoption_form)
            if form.is_valid():
                action = request.POST.get('action')
                # questionnaire = SubmittedAdoptionSurvey.objects.get(pk=self.kwargs['pk'])
                if action == 'adopt':
                    animal = submitted_adoption_form.animal
                    photos = AnimalPhotos.objects.filter(animal=animal.pk)
                    animal_data = animal.__dict__.copy()
                    [animal_data.pop(key) for key in ('_state', 'id')]
                    adopter_data = {
                        'email': form.cleaned_data['email'],
                        'phone_number': form.cleaned_data['phone_number']
                    }
                    questionnaire_data = {name: value for name, value in form.cleaned_data.items()
                                          if name not in adopter_data.keys()}
                    archived_animal = AdoptedAnimalsArchive.objects.create(questionnaire_text=questionnaire_data,
                                                                           **animal_data, **adopter_data)

                    for photo in photos:
                        photo_data = photo.__dict__.copy()
                        [photo_data.pop(key) for key in ('_state', 'id')]
                        photo_instance = AdoptedAnimalPhotosArchive(**photo_data)
                        photo_instance.animal = archived_animal
                        photo_instance.save()
                        AnimalPhotos.delete(photo)

                    Animal.delete(animal)
                elif action == 'reject':
                    submitted_adoption_form.status = 'rejected'
                    submitted_adoption_form.delete()

                return redirect(reverse_lazy('dashboard', kwargs={'slug': request.user.organization.slug}))
            return render(request, 'waiting-for-approval-details.html', {'form': form})
        else:
            raise PermissionDenied


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
