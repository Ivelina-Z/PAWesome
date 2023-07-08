from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy

from django.views.generic import CreateView, DetailView

from PAWesome.animal.models import Animal
from PAWesome.organization.forms import AnimalFrom
from PAWesome.organization.models import Organization


def view_all_organizations(request):
    return render(request, 'all-organizations.html')


def view_organization(request, slug):
    return render(request, 'organization-details.html')


class DashboardView(LoginRequiredMixin, DetailView):
    login_url = 'organization-login'
    model = Organization
    template_name = 'dashboard.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(pk=self.request.user.organization.pk)


def all_animals(request):
    return render(request, 'animals.html')


# TODO: Manually written URLs are shown for the other users than the signed
class AddPetView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    template_name = 'pet-add.html'
    model = Animal
    form_class = AnimalFrom

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.instance.organization = self.request.user.organization
        return form

    def get_success_url(self):
        return reverse_lazy('dashboard', kwargs={'pk': self.request.user.organization.pk})


def edit_pet(request):
    return render(request, 'pet-edit.html')


# def login_organization(request):
#     return render(request, 'login.html')
