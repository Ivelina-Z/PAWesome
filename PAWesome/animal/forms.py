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
    BOOLEAN_CHOICES = [
        (True, 'Да'),
        (False, 'Не'),
        (None, 'Неизвестно'),
        ('all', 'Всички')
    ]

    GENDER_CHOICES_WITH_ALL = Animal.GENDER_CHOICES
    GENDER_CHOICES_WITH_ALL.append(('all', 'Всички'))

    ANIMAL_TYPE_WITH_ALL = Animal.ANIMAL_TYPES
    ANIMAL_TYPE_WITH_ALL.append(('all', 'Всички'))

    animal_type = forms.ChoiceField(
        required=False,
        choices=Animal.ANIMAL_TYPES,
        label='Вид'
    )

    gender = forms.ChoiceField(
        required=False,
        choices=GENDER_CHOICES_WITH_ALL,
        label='Пол'
    )

    sprayed = forms.ChoiceField(
        required=False,
        choices=BOOLEAN_CHOICES,
        label='Кастриран/а'
    )

    vaccinated = forms.ChoiceField(
        required=False,
        choices=BOOLEAN_CHOICES,
        label='Ваксиниран/а'
    )
