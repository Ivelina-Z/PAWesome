from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from django.views.generic import CreateView
from PAWesome.organization.forms import OrganizationForm
from PAWesome.organization.models import Organization


def view_all_organizations(request):
    return render(request, 'all-organizations.html')


def view_organization(request, slug):
    return render(request, 'organization-details.html')


def dashboard(request):
    return render(request, 'dashboard.html')


def all_animals(request):
    return render(request, 'animals.html')


def add_pet(request):
    return render(request, 'pet-add.html')


def edit_pet(request):
    return render(request, 'pet-edit.html')


# def login_organization(request):
#     return render(request, 'login.html')
