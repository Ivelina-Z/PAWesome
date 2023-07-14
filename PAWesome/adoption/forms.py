from django import forms


class AdoptionSurveyForm(forms.Form):
    question = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Напишете въпрос за анкета'}),
        label=''
    )
