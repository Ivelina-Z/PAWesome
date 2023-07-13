from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from PAWesome.auth_app.forms import OrganizationRegistrationForm, EmployeeRegistrationForm
from PAWesome.organization.mixins import OrganizationMixin


UserModel = get_user_model()


class RegisterOrganizationView(CreateView):
    model = UserModel
    form_class = OrganizationRegistrationForm
    template_name = 'register.html'
    success_url = reverse_lazy('homepage')


class RegisterEmployeeView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ['organization.add_employee', 'auth.add_user']
    login_url = 'organization-login'
    model = UserModel
    form_class = EmployeeRegistrationForm
    template_name = 'register.html'
    success_url = reverse_lazy('homepage')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request_user'] = self.request.user
        return kwargs


class ConfirmRegistration(UpdateView):
    model = UserModel
    fields = []
    template_name = 'email-verification.html'
    success_url = reverse_lazy('login')

    def get_object(self, queryset=None):
        token = self.kwargs.get('token')
        try:
            user = self.model.objects.get(confirmation_token=token)
        except self.model.DoesNotExist:
            raise Http404('Invalid ot expired token.')

        user.is_active = True
        user.save()
        user.confirmation_token = ''

        return user


class OrganizationLoginView(OrganizationMixin, LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('dashboard', kwargs={'pk': self.get_organization().pk})
