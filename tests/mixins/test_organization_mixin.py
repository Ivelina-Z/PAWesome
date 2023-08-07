from django.test import TestCase
from django.test.client import RequestFactory

from PAWesome.mixins import OrganizationMixin
from tests.setup import _create_user_with_organization_profile, _create_user_with_employee_profile


class TestFormControlMixin(TestCase):
    def setUp(self):
        self.organization_user, self.organization, _ = _create_user_with_organization_profile()
        self.employee_user, self.employee, _ = _create_user_with_employee_profile(self.organization)

        self.organization_request = RequestFactory().get('')
        self.organization_request.user = self.organization_user

        self.employee_request = RequestFactory().get('')
        self.employee_request.user = self.employee_user

    def test__get_organization_with_organization_user__should_return_organization(self):
        mixin = OrganizationMixin(request=self.organization_request)
        organization = mixin.get_organization()
        self.assertEquals(organization, self.organization)

    def test__get_organization_with_employee_user__should_return_organization(self):
        mixin = OrganizationMixin(request=self.employee_request)
        organization = mixin.get_organization()
        self.assertEquals(organization, self.organization)

    def test__get_employee_with_employee_user__should_return_employee(self):
        mixin = OrganizationMixin(request=self.employee_request)
        employee = mixin.get_employee()
        self.assertEquals(employee, self.employee)

    def test__is_organization_with_organization_user__should_return_true(self):
        mixin = OrganizationMixin(request=self.organization_request)
        is_organization = mixin.is_organization()
        self.assertTrue(is_organization)

    def test__is_organization_with_employee_user__should_return_false(self):
        mixin = OrganizationMixin(request=self.employee_request)
        is_organization = mixin.is_organization()
        self.assertFalse(is_organization)

    def test__is_employee_with_organization_user__should_return_false(self):
        mixin = OrganizationMixin(request=self.organization_request)
        is_employee = mixin.is_employee()
        self.assertFalse(is_employee)

    def test__is_employee_with_employee_user__should_return_true(self):
        mixin = OrganizationMixin(request=self.employee_request)
        is_employee = mixin.is_employee()
        self.assertTrue(is_employee)
