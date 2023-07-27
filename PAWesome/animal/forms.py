from django import forms
from django.forms import FileInput, BaseInlineFormSet

from PAWesome.animal.models import Animal, AnimalPhotos
from PAWesome.mixins import FormControlMixin


class AnimalForm(FormControlMixin, forms.ModelForm):
    formset = None

    class Meta:
        model = Animal
        exclude = ['date_of_publication', 'organization', 'slug']
        widgets = {
            'location': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['foster_home'].widget.attrs['disabled'] = True
        self.fields['vet'].widget.attrs['disabled'] = True


class AnimalPhotoForm(FormControlMixin, forms.ModelForm):
    photo = forms.ImageField(widget=FileInput)

    class Meta:
        model = AnimalPhotos
        fields = '__all__'


# class AnimalPhotoInlineFormSet(BaseInlineFormSet):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.deletion_widget = CustomDeleteFormsetWidget


class FilterAnimalForm(FormControlMixin, forms.Form):
    animal_type = forms.ChoiceField(
        required=False,
        choices=Animal.ANIMAL_TYPES,
        label='Вид'
    )

    gender = forms.ChoiceField(
        required=False,
        choices=Animal.GENDER_CHOICES,
        label='Пол'
    )

    sprayed = forms.NullBooleanField(
        label='Кастриран/а'
    )

    medical_issues = forms.BooleanField(
        required=False,
        label='Медицински проблеми'
    )
