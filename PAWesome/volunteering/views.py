from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView, UpdateView

from PAWesome.mixins import OrganizationMixin, FormControlMixin
from PAWesome.volunteering.forms import DonationForm, DeliveryInfoForm, FosterHomeForm, FilterDonationTicketsForm
from PAWesome.volunteering.models import DonationsDeliveryInfo, DonationTickets, FosterHome
from PAWesome.volunteering.token import Token


# PUBLIC

def how_to_help(request):
    return render(request, 'how-to-help.html')


class ViewFosterHomes(LoginRequiredMixin, ListView):
    login_url = 'login'
    template_name = 'foster_home/foster-homes.html'
    model = FosterHome


class AddFosterHome(SuccessMessageMixin, CreateView):
    template_name = 'foster_home/foster-home-add.html'
    model = FosterHome
    form_class = FosterHomeForm
    success_url = reverse_lazy('homepage')
    success_message = 'Успешно се записахте като приемен дом.'


class EditFosterHome(SuccessMessageMixin, UpdateView):
    template_name = 'foster_home/foster-home-edit.html'
    model = FosterHome
    form_class = FosterHomeForm
    success_url = reverse_lazy('homepage')
    success_message = 'Промените са записани успешно.'

    def get_object(self, queryset=None):
        token = self.kwargs.get('token')
        user = Token.check_token(self.model, token)
        # try:
        #     user = self.model.objects.get(token=token)
        # except self.model.DoesNotExist:
        #     raise Http404('Invalid token.')
        return user


class DeleteFosterHome(SuccessMessageMixin, DeleteView):
    template_name = 'foster_home/foster-home-delete.html'
    model = FosterHome
    success_url = reverse_lazy('homepage')
    success_message = 'Вашият приемен дом е успешно изтрит.'

    def get_object(self, queryset=None):
        token = self.kwargs.get('token')
        user = Token.check_token(self.model, token)
        return user


class DeliveryInfoView(LoginRequiredMixin, ListView):
    login_url = 'login'
    template_name = 'delivery_info/delivery-info.html'
    model = DonationsDeliveryInfo


class AddDeliveryInfoView(OrganizationMixin, LoginRequiredMixin, CreateView):
    login_url = 'login'
    template_name = 'delivery_info/delivery-info-add.html'
    model = DonationsDeliveryInfo
    form_class = DeliveryInfoForm

    def form_valid(self, form):
        form.instance.organization = self.get_organization()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('dashboard', kwargs={'slug': self.get_organization().slug})


class EditDeliveryInfoView(OrganizationMixin, LoginRequiredMixin, UpdateView):
    login_url = 'login'
    template_name = 'delivery_info/delivery-info-edit.html'
    model = DonationsDeliveryInfo
    form_class = DeliveryInfoForm

    def get_success_url(self):
        return reverse_lazy('dashboard', kwargs={'slug': self.get_organization().slug})


class DeleteDeliveryInfoView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = ['volunteering.delete_donationsdeliveryinfo']
    login_url = 'login'
    template_name = 'delivery_info/delivery-info-delete.html'
    success_url = reverse_lazy('delivery-info')
    model = DonationsDeliveryInfo


class FoodDonationView(ListView):
    template_name = 'donation_ticket/donation-tickets.html'
    model = DonationTickets

    def get_queryset(self):
        queryset = super().get_queryset()

        form = FilterDonationTicketsForm(self.request.GET)

        if form.is_valid():
            filters = {}
            for field_name, field_value in form.cleaned_data.items():
                if field_name is not None and field_value != '':
                    filters[field_name] = field_value
            queryset = self.model.objects.filter(**filters)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['form'] = FilterDonationTicketsForm(self.request.GET)
        return context


class AddDonationTicket(OrganizationMixin, LoginRequiredMixin, CreateView):
    login_url = 'login'
    template_name = 'donation_ticket/donation-ticket-add.html'
    model = DonationTickets
    form_class = DonationForm

    def form_valid(self, form):
        form.instance.created_by = self.get_organization()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('dashboard', kwargs={'slug': self.get_organization().slug})


class EditDonationTickets(OrganizationMixin, LoginRequiredMixin, UpdateView):
    login_url = 'login'
    template_name = 'donation_ticket/donation-ticket-edit.html'
    model = DonationTickets
    form_class = DonationForm

    def get_success_url(self):
        return reverse_lazy('dashboard', kwargs={'slug': self.get_organization().slug})


class DeleteDonationTicket(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = ['volunteering.delete_donationtickets']
    login_url = 'login'
    template_name = 'donation_ticket/donation-ticket-delete.html'
    success_url = reverse_lazy('donation-tickets')
    model = DonationTickets

