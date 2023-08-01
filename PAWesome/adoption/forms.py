from django import forms
from django.forms import JSONField
from phonenumber_field.formfields import PhoneNumberField


class AdoptionSurveyForm(forms.Form):
    question = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Напишете въпрос за анкета'}),
        label='',
        error_messages={"required": "The field can't be empty."}
    )


class FilledAdoptionForm(forms.Form):
    email = forms.EmailField()
    phone_number = PhoneNumberField()
