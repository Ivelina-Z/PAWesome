from django import forms
from django.forms import FileInput, BaseInlineFormSet

from PAWesome.animal.models import Animal, AnimalPhotos
from PAWesome.animal.custom_widgets import CustomDeleteFormsetWidget
from PAWesome.mixins import FormControlMixin


class AnimalForm(FormControlMixin, forms.ModelForm):
    formset = None

    class Meta:
        model = Animal
        exclude = ['date_of_publication', 'organization', 'slug']
        widgets = {
            'location': forms.HiddenInput()
        }


class AnimalPhotoForm(FormControlMixin, forms.ModelForm):
    photo = forms.ImageField(widget=FileInput)

    class Meta:
        model = AnimalPhotos
        fields = '__all__'


class AnimalPhotoInlineFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.deletion_widget = CustomDeleteFormsetWidget
