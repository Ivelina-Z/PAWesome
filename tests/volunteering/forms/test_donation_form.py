from django.core.exceptions import ValidationError
from django.test import TestCase

from PAWesome.volunteering.forms import DonationForm
from PAWesome.volunteering.models import DonationsDeliveryInfo
from tests.setup import _create_delivery_info, _create_user_with_organization_profile


class TestDonationForm(TestCase):
    def setUp(self):
        _, self.organization, _ = _create_user_with_organization_profile()
        self.delivery_info = _create_delivery_info(self.organization)

    def test__donation_ticket_form_valid_data__form_should_be_valid(self):

        valid_form_data = {
            'category': 'food',
            'item': 'Test Food',
            'weight_quantity': 2.0,
            'count_quantity': 0,
            'delivery_info': [self.delivery_info.pk]
        }
        form = DonationForm(data=valid_form_data)
        self.assertTrue(form.is_valid())

    def test__donation_ticket_both_weight_and_quantity__form_with_error(self):
        invalid_form_data_both_quantity = {
            'category': 'food',
            'item': 'Test Food',
            'weight_quantity': 2.0,
            'count_quantity': 2,
            'delivery_info': [self.delivery_info.pk]
        }
        form = DonationForm(data=invalid_form_data_both_quantity)
        self.assertFalse(form.is_valid())

        self.assertIn(DonationForm.ERROR_MESSAGE_ONE_TYPE_OF_QUANTITY, form.errors['__all__'])

    def test__donation_ticket_no_quantity__form_with_error(self):
        invalid_form_data_no_quantity = {
            'category': 'food',
            'item': 'Test Food',
            'weight_quantity': 0.0,
            'count_quantity': 0,
            'delivery_info': [self.delivery_info.pk]
        }
        form = DonationForm(data=invalid_form_data_no_quantity)
        self.assertFalse(form.is_valid())

        self.assertIn(DonationForm.ERROR_MESSAGE_ONE_TYPE_OF_QUANTITY, form.errors['__all__'])

    # def test__donation_ticket_no_delivery_info__raise_validation_error(self):
    #     self.delivery_info.delete()
    #     invalid_form_data_no_delivery_address = {
    #         'category': 'food',
    #         'item': 'Test Food',
    #         'weight_quantity': 2.0,
    #         'count_quantity': 0,
    #         'delivery_info': DonationsDeliveryInfo.objects.all()
    #     }
    #
    #     with self.assertRaises(ValidationError) as e:
    #         form = DonationForm(data=invalid_form_data_no_delivery_address)
    #     self.assertIn(DonationForm.ERROR_MESSAGE_AT_LEAST_ONE_ADDRESS, e.exception.message)
