from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView, PasswordChangeView
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView

from PAWesome import settings
from PAWesome.auth_app.forms import OrganizationRegistrationForm, EmployeeRegistrationForm, LoginForm
from PAWesome.mixins import OrganizationMixin

UserModel = get_user_model()


class RegisterOrganizationView(CreateView):
    model = UserModel
    form_class = OrganizationRegistrationForm
    template_name = 'register.html'
    success_url = reverse_lazy('homepage')


class RegisterEmployeeView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ['organization.add_employee', 'auth_app.add_customuser']
    login_url = 'login'
    model = UserModel
    form_class = EmployeeRegistrationForm
    template_name = 'register.html'
    success_url = reverse_lazy('homepage')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request_user'] = self.request.user
        return kwargs


class ConfirmRegistration(View):
    model = UserModel

    def get(self, request, *args, **kwargs):
        token = self.kwargs.get('token')
        try:
            user = self.model.objects.get(confirmation_token=token)
        except self.model.DoesNotExist:
            raise Http404('Invalid ot expired token.')

        user.is_active = True
        user.confirmation_token = ''
        user.save()
        return redirect(reverse_lazy('login'))


class CustomLoginView(OrganizationMixin, LoginView):
    template_name = 'login.html'
    form_class = LoginForm

    def get_success_url(self):
        return reverse_lazy('dashboard', kwargs={'slug': self.get_organization().slug})


class ResetPassword(PasswordResetView):
    template_name = 'reset-password.html'
    html_email_template_name = 'reset-password-email.html'
    from_email = settings.EMAIL_HOST_USER
    success_url = reverse_lazy('homepage')


class ResetConfirmPassword(PasswordResetConfirmView):
    template_name = 'reset-password-confirm.html'
    success_url = reverse_lazy('login')


class PasswordChange(OrganizationMixin, PasswordChangeView):
    template_name = 'change-password.html'

    def get_success_url(self):
        return reverse_lazy('dashboard', kwargs={'slug': self.get_organization().slug})# class ChangePassword(UpdateView):
