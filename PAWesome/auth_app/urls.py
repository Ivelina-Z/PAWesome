from django.urls import path, include
from django.contrib.auth.views import LogoutView

from PAWesome.auth_app.views import RegisterOrganizationView, RegisterEmployeeView, \
    ConfirmRegistration, CustomLoginView

urlpatterns = [
    path('register/organization/', RegisterOrganizationView.as_view(), name='organization-register'),
    path('register/employee/', RegisterEmployeeView.as_view(), name='organization-register-employee'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registration/verify/<token>', ConfirmRegistration.as_view(), name='register-confirmation'),
]