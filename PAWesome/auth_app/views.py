from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import CreateView
from PAWesome.auth_app.forms import RegistrationForm

UserModel = get_user_model()


class RegisterOrganizationView(CreateView):
    model = UserModel
    form_class = RegistrationForm
    template_name = 'register.html'
    success_url = reverse_lazy('homepage')
