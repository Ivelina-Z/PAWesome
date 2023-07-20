from django.urls import path, include
from django.contrib.auth.views import LogoutView

from PAWesome.auth_app.views import RegisterOrganizationView, OrganizationLoginView, RegisterEmployeeView, \
    ConfirmRegistration

urlpatterns = [
    path('organization/', include([
        path('register/', include([
            path('', RegisterOrganizationView.as_view(), name='organization-register'),
            path('employee/', RegisterEmployeeView.as_view(), name='organization-register-employee'),
        ])),
    ])),
    path('login/', OrganizationLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registration/verify/<token>', ConfirmRegistration.as_view(), name='register-confirmation'),
]

# urlpatterns = [
#     path('organization/register/', RegisterOrganizationView.as_view(), name='organization-register'),
#     path('organization/login/', OrganizationLoginView.as_view(), name='organization-login'),
#     path('organization/logout/', LogoutView.as_view(), name='organization-logout')
# ]
