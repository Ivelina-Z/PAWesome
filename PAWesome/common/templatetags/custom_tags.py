from django import template
from django.contrib.auth.models import Group

from PAWesome.mixins import OrganizationMixin

register = template.Library()


# @register.filter(name='has_group')
# def has_group(user, group_name):
#     try:
#         group = Group.objects.get(name=group_name)
#     except Group.DoesNotExist:
#         return False
#     return True if group in user.groups.all() else False


@register.simple_tag
def get_organization(request):
    mixin = OrganizationMixin(request=request)
    return mixin.get_organization()


@register.simple_tag
def get_employee(request):
    mixin = OrganizationMixin(request=request)
    return mixin.get_employee()


@register.simple_tag
def is_employee(request):
    mixin = OrganizationMixin(request=request)
    return mixin.is_employee()


@register.simple_tag()
def is_organization(request):
    mixin = OrganizationMixin(request=request)
    return mixin.is_organization()
