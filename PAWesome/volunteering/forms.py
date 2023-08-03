from django import forms
from django.core.exceptions import ValidationError

from PAWesome.mixins import FormControlMixin
from PAWesome.volunteering.models import DonationTickets, DonationsDeliveryInfo, FosterHome


class DonationForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = DonationTickets
        exclude = ['created_by']
        help_texts = {
            'delivery_info': 'Повече от един адрес може да бъде избран.'
        }

    # TODO: Move the validation in the model with custom class validator

    def clean(self):
        if not self.cleaned_data['count_quantity'] and not self.cleaned_data['weight_quantity']:
            raise ValidationError("Either count quantity or weight quantity is required.")
        elif self.cleaned_data['count_quantity'] and self.cleaned_data['weight_quantity']:
            raise ValidationError("Only one of count quantity or weight quantity should be provided.")


class FilterDonationTicketsForm(FormControlMixin, forms.Form):
    category = forms.ChoiceField(
        required=False,
        choices=DonationTickets.CATEGORY_CHOICES,
        label='Категория'
    )


class DeliveryInfoForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = DonationsDeliveryInfo
        exclude = ['organization']


class FosterHomeForm(FormControlMixin, forms.ModelForm):
    ERROR_MESSAGE = "At least one of the available spots fields should be filled."

    class Meta:
        model = FosterHome
        exclude = ['token']
        widgets = {
            'location': forms.HiddenInput()
        }

    def clean(self):
        available_spots_fields = ['cat_available_spots', 'dog_available_spots', 'bunny_available_spots']
        if all(not self.cleaned_data[field] for field in available_spots_fields):
            raise ValidationError(self.ERROR_MESSAGE)


