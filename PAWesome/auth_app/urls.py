from django.urls import path
from django.contrib.auth.views import LogoutView

from PAWesome.auth_app.views import RegisterOrganizationView, OrganizationLoginView

urlpatterns = [
    path('organization/register/', RegisterOrganizationView.as_view(), name='organization-register'),
    path('organization/login/', OrganizationLoginView.as_view(), name='organization-login'),
    path('organization/logout/', LogoutView.as_view(), name='organization-logout')
]
