import json

from django import forms


class AdoptionSurveyForm(forms.Form):
    question = forms.CharField()


# class AdoptForm(forms.ModelForm):
#     pass
#     class Meta:
#         model = AdoptionSurvey
#         fields = ['question_text']
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # json_data = self.fields['question_text']
#         instance = kwargs.get('instance')
#         if instance:
#             json_data = instance.question_text
#         for name, field_value in json_data.items():
#             self.fields[name] = field_value
