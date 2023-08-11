from django.test import TestCase

from PAWesome.volunteering.forms import FosterHomeForm


class TestFosterHomeForm(TestCase):
    def test__foster_home_form_valid_data__form_should_be_valid(self):

        valid_form_data = {
            'phone_number': '0894112233',
            'email': 'test_foster_home@gmail.com',
            'cat_available_spots': 2,
            'dog_available_spots': 0,
            'bunny_available_spots': 0,
            'additional_info': '',
            'location': 'POINT(42.0 27.0)'
        }
        form = FosterHomeForm(data=valid_form_data)
        self.assertTrue(form.is_valid())

    def test__foster_home_form_invalid_data_no_available_spot__form_with_errors(self):
        invalid_form_data = {
            'phone_number': '0894112233',
            'email': 'test_foster_home@gmail.com',
            'cat_available_spots': 0,
            'dog_available_spots': 0,
            'bunny_available_spots': 0,
            'additional_info': '',
            'location': 'POINT(42.0 27.0)'
        }
        form = FosterHomeForm(data=invalid_form_data)
        self.assertFalse(form.is_valid())

        self.assertIn(FosterHomeForm.ERROR_MESSAGE, form.errors['__all__'])
