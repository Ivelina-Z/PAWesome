from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ValidationError
from django.forms import CharField, inlineformset_factory
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View

from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView

from PAWesome.adoption.forms import AdoptionSurveyForm, FilledAdoptionForm
from PAWesome.adoption.models import SubmittedAdoptionSurvey
from PAWesome.animal.models import Animal, AdoptedAnimalsArchive, AnimalPhotos, AdoptedAnimalPhotosArchive
from PAWesome.animal.views import BaseAdoptView
from PAWesome.mixins import FormControlMixin
from PAWesome.organization.forms import AnimalForm, AnimalPhotoForm, OrganizationForm, EmployeeForm
from PAWesome.organization.mixins import OrganizationMixin
from PAWesome.organization.models import Organization, Employee


# PUBLIC PART

def view_all_organizations(request):
    return render(request, 'all-organizations.html')


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


# TODO: Manually written URLs are shown for the other users than the signed
class AddAnimalView(SuccessMessageMixin, OrganizationMixin, LoginRequiredMixin, CreateView):
    login_url = 'login'
    success_message = 'The animal is added successfully.'
    template_name = 'animal-add.html'
    model = Animal
    form_class = AnimalForm
    AnimalPhotoFormSet = inlineformset_factory(Animal, AnimalPhotos, form=AnimalPhotoForm, extra=1, can_delete=False)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if self.request.method == 'POST':
            form.formset = self.AnimalPhotoFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            form.formset = self.AnimalPhotoFormSet(instance=self.object)
        return form

    def form_valid(self, form):
        form.instance.organization = self.get_organization()
        if form.formset.is_valid() and form.is_valid():
            form.save()
            formset = form.formset
            instances = formset.save(commit=False)
            for instance in instances:
                instance.is_main_image = True
                instance.animal = form.instance
                instance.save()
            return super().form_valid(form)

    def get_success_url(self):
        organization = self.get_organization()
        return reverse_lazy('dashboard', kwargs={'slug': organization.slug})


class EditAnimalView(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    template_name = 'animal-edit.html'
    model = Animal
    form_class = AnimalForm
    AnimalPhotoFormSet = inlineformset_factory(Animal, AnimalPhotos, form=AnimalPhotoForm, extra=0)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if self.request.method == 'POST':
            form.formset = self.AnimalPhotoFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            form.formset = self.AnimalPhotoFormSet(instance=self.object)
        return form

    def form_valid(self, form):
        # photos = AnimalPhotos.objects.get(animal=self.object.pk)
        formset = form.formset
        if form.is_valid() and formset.is_valid():
            total_main_images = 0
            for instance in formset:
                if instance.cleaned_data['is_main_image']:
                    total_main_images += 1
                if total_main_images > 1:
                    raise ValidationError('The main image can be only ONE.')
            form.save()
            formset.save()
            return super().form_valid(form)
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('animal-details', kwargs={'pk': self.object.pk})


class DeleteAnimalView(OrganizationMixin, PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    login_url = 'login'
    permission_required = ['animal.delete_animal', 'animal.delete_animalphotos']
    template_name = 'animal-delete.html'
    model = Animal

    def get_success_url(self):
        organization = self.get_organization()
        return reverse_lazy('organization-animals', kwargs={'slug': organization.slug})


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
            questionnaire = SubmittedAdoptionSurvey.objects.get(pk=kwargs['pk'])
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
                questionnaire.delete()
                # except:

            return redirect(reverse_lazy('dashboard', kwargs={'slug': request.user.organization.slug}))
        return render(request, 'waiting-for-approval-details.html', {'form': form})


class ViewProfile(OrganizationMixin, LoginRequiredMixin, DetailView):
    login_url = 'login'
    template_name = 'view-profile.html'

    def get_object(self, queryset=None):
        if self.is_organization():
            model = Organization
        elif self.is_employee():
            model = Employee


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
