from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy

from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView

from PAWesome.animal.models import Animal
from PAWesome.animal.views import BaseAdoptView
from PAWesome.organization.forms import AnimalForm
from PAWesome.organization.models import Organization


# PUBLIC PART

def view_all_organizations(request):
    return render(request, 'all-organizations.html')


def view_organization(request, slug):
    return render(request, 'organization-details.html')


# PRIVATE PART


class DashboardView(LoginRequiredMixin, DetailView):
    login_url = 'organization-login'
    model = Organization
    template_name = 'dashboard.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(pk=self.request.user.organization.pk)


class AllAnimalsView(LoginRequiredMixin, BaseAdoptView):
    login_url = 'login'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(organization=self.request.user.organization.pk).prefetch_related('photos')


# TODO: Manually written URLs are shown for the other users than the signed
class AddPetView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    template_name = 'pet-add.html'
    model = Animal
    form_class = AnimalForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.instance.organization = self.request.user.organization
        return form

    def get_success_url(self):
        return reverse_lazy('dashboard', kwargs={'pk': self.request.user.organization.pk})


class EditPetView(LoginRequiredMixin, UpdateView):
    login_url = 'login'

    template_name = 'pet-edit.html'
    model = Animal
    form_class = AnimalForm

    def get_success_url(self):
        return reverse_lazy('animal-details', kwargs={'pk': self.object.pk})


class DeletePetView(LoginRequiredMixin, DeleteView):
    login_url = 'login'
    template_name = 'pet-delete.html'
    model = Animal

    def get_success_url(self):
        return reverse_lazy('organization-animals', kwargs={'pk': self.request.user.organization.pk})
