from django import forms
from django.core.exceptions import ValidationError
from django.http import Http404

from PAWesome.mixins import FormControlMixin
from PAWesome.volunteering.models import DonationTickets, DonationsDeliveryInfo, FosterHome


class DonationForm(FormControlMixin, forms.ModelForm):
    ERROR_MESSAGE_AT_LEAST_ONE_ADDRESS = 'Поне един адрес за доставка трябва да бъде създаден.'
    ERROR_MESSAGE_ONE_TYPE_OF_QUANTITY = 'Попълнете един от параметрите за количество - тегло ИЛИ брой.'

    class Meta:
        model = DonationTickets
        exclude = ['created_by']
        help_texts = {
            'delivery_info': 'Повече от един адрес може да бъде избран.'
        }

    def __init__(self, organization=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if organization:
            self.fields['delivery_info'].queryset = self.fields['delivery_info'].queryset.filter(
                organization=organization)
        if not self.fields['delivery_info'].queryset:
            raise Http404(self.ERROR_MESSAGE_AT_LEAST_ONE_ADDRESS)

    def clean(self):
        if not self.cleaned_data['count_quantity'] and not self.cleaned_data['weight_quantity']:
            raise ValidationError(self.ERROR_MESSAGE_ONE_TYPE_OF_QUANTITY)
        elif self.cleaned_data['count_quantity'] and self.cleaned_data['weight_quantity']:
            raise ValidationError(self.ERROR_MESSAGE_ONE_TYPE_OF_QUANTITY)


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
    ERROR_MESSAGE = "Минимум едно свободно място за животно трябва да бъде въведено."

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


