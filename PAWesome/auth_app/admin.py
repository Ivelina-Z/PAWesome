from functools import partial

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from PAWesome.auth_app.forms import EmployeeRegistrationForm
from PAWesome.auth_app.views import RegisterEmployeeView

UserModel = get_user_model()


@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, change=False, **kwargs):
        if obj is None:
            return EmployeeRegistrationForm
        else:
            return super().get_form(request, obj, change, **kwargs)

    def save_model(self, request, obj, form, change):
        if not change:
            obj = RegisterEmployeeView._create_user_with_employee_profile(form, request)
        return super().save_model(request, obj, form, change)
