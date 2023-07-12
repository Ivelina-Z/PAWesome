from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured
from django.forms import CharField, formset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View

from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView

from PAWesome.adoption.forms import AdoptionSurveyForm
from PAWesome.adoption.models import SubmittedAdoptionSurvey
from PAWesome.animal.models import Animal, AdoptedAnimalsArchive
from PAWesome.animal.views import BaseAdoptView
from PAWesome.organization.forms import AnimalForm
from PAWesome.organization.models import Organization
from PAWesome.volunteering.views import BaseFoodDonationView


# PUBLIC PART

def view_all_organizations(request):
    return render(request, 'all-organizations.html')


def view_organization(request, slug):
    return render(request, 'organization-details.html')


# PRIVATE PART
class FoodDonationView(LoginRequiredMixin, BaseFoodDonationView):
    login_url = 'organization-login'


class DashboardView(LoginRequiredMixin, DetailView):
    login_url = 'organization-login'
    model = Organization
    template_name = 'dashboard.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(pk=self.request.user.organization.pk)


class AllAnimalsView(LoginRequiredMixin, BaseAdoptView):
    login_url = 'organization-login'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(organization=self.request.user.organization.pk).prefetch_related('photos')


# TODO: Manually written URLs are shown for the other users than the signed
class AddAnimalView(LoginRequiredMixin, CreateView):
    login_url = 'organization-login'
    template_name = 'animal-add.html'
    model = Animal
    form_class = AnimalForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.instance.organization = self.request.user.organization
        return form

    def get_success_url(self):
        return reverse_lazy('dashboard', kwargs={'pk': self.request.user.organization.pk})


class EditAnimalView(LoginRequiredMixin, UpdateView):
    login_url = 'organization-login'

    template_name = 'animal-edit.html'
    model = Animal
    form_class = AnimalForm

    def get_success_url(self):
        return reverse_lazy('animal-details', kwargs={'pk': self.object.pk})


class DeleteAnimalView(LoginRequiredMixin, DeleteView):
    login_url = 'organization-login'
    template_name = 'animal-delete.html'
    model = Animal

    def get_success_url(self):
        return reverse_lazy('organization-animals', kwargs={'pk': self.request.user.organization.pk})


class AllWaitingForApproval(LoginRequiredMixin, ListView):
    login_url = 'organization-login'
    template_name = 'waiting-for-approval.html'
    model = SubmittedAdoptionSurvey

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(organization=self.request.user.organization.pk)


class WaitingForApprovalDetails(LoginRequiredMixin, View):
    login_url = 'organization-login'

    def get(self, request, *args, **kwargs):
        form = AdoptionSurveyForm()

        # TODO: Create is as a method to the Form so it can be reused.
        json_data = get_object_or_404(SubmittedAdoptionSurvey, animal=kwargs['animal_pk']).questionnaire_text
        for field_name, field_value in json_data.items():
            form.fields[field_name] = CharField(initial=field_value, disabled=True)
        return render(request, 'waiting-for-approval-details.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = AdoptionSurveyForm(self.request.POST)
        if form.is_valid():
            adopted_animal = AdoptedAnimalsArchive()
            animal = get_object_or_404(Animal, pk=kwargs['animal_pk'])
            questionnaire = get_object_or_404(SubmittedAdoptionSurvey, animal=kwargs['animal_pk'])
            for field in animal._meta.fields:
                setattr(adopted_animal, field.name, getattr(animal, field.name))
            adopted_animal.filled_questionnaire_text = form.cleaned_data
            adopted_animal.save()

            Animal.delete(animal)

            return redirect(reverse_lazy('dashboard', kwargs={'pk': request.user.organization.pk}))
        return render(request, 'waiting-for-approval-details.html', {'form': form})
