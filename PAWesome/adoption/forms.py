from django import forms
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import RegionalPhoneNumberWidget


class AdoptionSurveyForm(forms.Form):
    question = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Напишете въпрос за анкета'}),
        label='',
        error_messages={"required": "The field can't be empty."}
    )


class FilledAdoptionForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone_number = PhoneNumberField(widget=RegionalPhoneNumberWidget(attrs={'class': 'form-control'}))
