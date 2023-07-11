from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView, UpdateView

from PAWesome.volunteering.forms import FoodDonationForm, DeliveryInfoForm
from PAWesome.volunteering.models import DonationsDeliveryInfo, FoodDonationTickets


class BaseFoodDonationView(ListView):
    template_name = 'food-donation.html'
    model = FoodDonationTickets


def donate(request):
    return render(request, 'donate.html')


def add_foster_home(request):
    return render(request, 'foster-home.html')


def view_foster_homes(request):
    return render(request, 'foster-homes-details.html')


def how_to_help(request):
    return render(request, 'how-to-help.html')


class FoodDonationView(BaseFoodDonationView):
    pass

# PRIVATE


class DeliveryInfoView(LoginRequiredMixin, ListView):
    login_url = 'login'
    template_name = 'delivery-info.html'
    model = DonationsDeliveryInfo


class AddDeliveryInfoView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    template_name = 'delivery-info-add.html'
    model = DonationsDeliveryInfo
    form_class = DeliveryInfoForm

    def form_valid(self, form):
        form.instance.organization = self.request.user.organization
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('dashboard', kwargs={'pk': self.request.user.organization.pk})


class EditDeliveryInfoView(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    template_name = 'delivery-info-edit.html'
    model = DonationsDeliveryInfo
    form_class = DeliveryInfoForm

    def get_success_url(self):
        return reverse_lazy('dashboard', kwargs={'pk': self.request.user.organization.pk})





class AddFoodDonation(LoginRequiredMixin, CreateView):
    login_url = 'login'
    template_name = 'food-donation-add.html'
    model = FoodDonationTickets
    form_class = FoodDonationForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user.organization
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('dashboard', kwargs={'pk': self.request.user.organization.pk})


class EditFoodDonation(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    template_name = 'food-donation-edit.html'
    model = FoodDonationTickets
    form_class = FoodDonationForm

    def get_success_url(self):
        return reverse_lazy('dashboard', kwargs={'pk': self.request.user.organization.pk})


# class DeleteDeliveryInfoView(LoginRequiredMixin, DeleteView):
#     pass
