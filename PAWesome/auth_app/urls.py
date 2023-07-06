from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from PAWesome.auth_app.views import RegisterOrganizationView

urlpatterns = [
    path('organization/register/', RegisterOrganizationView.as_view(), name='organization-register'),
    path('organization/login/', LoginView.as_view(template_name='login.html'), name='organization-login'),
    path('organization/logout/', LogoutView.as_view(), name='organization-logout')
]
