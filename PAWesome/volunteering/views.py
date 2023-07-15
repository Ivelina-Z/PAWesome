from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView, UpdateView

from PAWesome.organization.mixins import OrganizationMixin
from PAWesome.volunteering.forms import DonationForm, DeliveryInfoForm, FosterHomeForm
from PAWesome.volunteering.models import DonationsDeliveryInfo, DonationTickets, FosterHome


# PUBLIC

def how_to_help(request):
    return render(request, 'how-to-help.html')


class FosterHomes(LoginRequiredMixin, ListView):
    login_url = 'login'
    template_name = 'foster-homes.html'
    model = FosterHome


class AddFosterHome(CreateView):
    template_name = 'foster-home-add.html'
    model = FosterHome
    form_class = FosterHomeForm
    success_url = reverse_lazy('homepage')


class EditFosterHome(UpdateView):
    template_name = 'foster-home-edit.html'
    model = FosterHome
    form_class = FosterHomeForm
    success_url = reverse_lazy('homepage')

    def get_object(self, queryset=None):
        token = self.kwargs.get('token')
        try:
            user = self.model.objects.get(token=token)
        except self.model.DoesNotExist:
            raise Http404('Invalid token.')
        return user


class DeleteFosterHome(DeleteView):
    template_name = 'foster-home-delete.html'
    model = FosterHome
    success_url = reverse_lazy('homepage')

    def get_object(self, queryset=None):
        token = self.kwargs.get('token')
        try:
            user = self.model.objects.get(token=token)
        except self.model.DoesNotExist:
            raise Http404('Invalid token.')
        return user


class DeliveryInfoView(LoginRequiredMixin, ListView):
    login_url = 'login'
    template_name = 'delivery-info.html'
    model = DonationsDeliveryInfo


class AddDeliveryInfoView(OrganizationMixin, LoginRequiredMixin, CreateView):
    login_url = 'login'
    template_name = 'delivery-info-add.html'
    model = DonationsDeliveryInfo
    form_class = DeliveryInfoForm

    def form_valid(self, form):
        form.instance.organization = self.get_organization()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('dashboard', kwargs={'slug': self.get_organization().slug})


class EditDeliveryInfoView(OrganizationMixin, LoginRequiredMixin, UpdateView):
    login_url = 'login'
    template_name = 'delivery-info-edit.html'
    model = DonationsDeliveryInfo
    form_class = DeliveryInfoForm

    def get_success_url(self):
        return reverse_lazy('dashboard', kwargs={'slug': self.get_organization().slug})


class DeleteDeliveryInfoView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = ['volunteering.delete_donationsdeliveryinfo']
    login_url = 'login'
    template_name = 'delivery-info-delete.html'
    success_url = reverse_lazy('delivery-info')
    model = DonationsDeliveryInfo


class FoodDonationView(ListView):
    template_name = 'donation-tickets.html'
    model = DonationTickets


class AddDonationTicket(OrganizationMixin, LoginRequiredMixin, CreateView):
    login_url = 'login'
    template_name = 'donation-ticket-add.html'
    model = DonationTickets
    form_class = DonationForm

    def form_valid(self, form):
        form.instance.created_by = self.get_organization()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('dashboard', kwargs={'slug': self.get_organization().slug})


class EditDonationTickets(OrganizationMixin, LoginRequiredMixin, UpdateView):
    login_url = 'login'
    template_name = 'donation-ticket-edit.html'
    model = DonationTickets
    form_class = DonationForm

    def get_success_url(self):
        return reverse_lazy('dashboard', kwargs={'slug': self.get_organization().slug})


class DeleteDonationTicket(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = ['volunteering.delete_donationtickets']
    login_url = 'login'
    template_name = 'donation-ticket-delete.html'
    success_url = reverse_lazy('donation-ticket')
    model = DonationTickets
