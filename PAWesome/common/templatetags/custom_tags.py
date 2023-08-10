from django import template

from PAWesome.mixins import OrganizationMixin

register = template.Library()


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
