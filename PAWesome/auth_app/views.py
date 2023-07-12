from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User, Group
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from PAWesome.auth_app.forms import OrganizationRegistrationForm, EmployeeRegistrationForm


class RegisterOrganizationView(CreateView):
    model = User
    form_class = OrganizationRegistrationForm
    template_name = 'register.html'
    success_url = reverse_lazy('homepage')


class RegisterEmployeeView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ['organization.add_employee', 'auth.add_user']
    login_url = 'organization-login'
    model = User
    form_class = EmployeeRegistrationForm
    template_name = 'register.html'
    success_url = reverse_lazy('homepage')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request_user'] = self.request.user
        return kwargs


class OrganizationLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        is_organization_group = self.request.user.groups.filter(name='Organizations').exists() # TODO: Implement as mixin to return the group name
        if self.request.user.is_authenticated and is_organization_group:
            return reverse_lazy('dashboard', kwargs={'pk': self.request.user.organization.pk})
        elif self.request.user.is_authenticated and not is_organization_group:
            return reverse_lazy('dashboard', kwargs={'pk': self.request.user.employee.organization.pk})
