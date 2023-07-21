from django.urls import path, include
from django.contrib.auth.views import LogoutView, PasswordResetConfirmView, PasswordChangeView

from PAWesome.auth_app.views import RegisterOrganizationView, RegisterEmployeeView, \
    ConfirmRegistration, CustomLoginView, ResetPassword, ResetConfirmPassword, PasswordChange

urlpatterns = [
    path('register/organization/', RegisterOrganizationView.as_view(), name='organization-register'),
    path('register/employee/', RegisterEmployeeView.as_view(), name='organization-register-employee'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registration/verify/<token>', ConfirmRegistration.as_view(), name='register-confirmation'),
    path('password/', include([
        path('reset/', ResetPassword.as_view(), name='password-reset'),
        path('reset/<uidb64>/<token>', ResetConfirmPassword.as_view(), name='password-reset-confirm'),
        path('change/', PasswordChange.as_view(), name='password-change'),
    ])),

    # path('profile/change-password/<token>', ChangePassword.as_view(), name='password-change'),
]