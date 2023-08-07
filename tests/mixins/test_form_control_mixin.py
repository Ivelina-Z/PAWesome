from django.forms import Form, CharField, CheckboxInput
from django.test import TestCase
from PAWesome.mixins import FormControlMixin


class TestFormControlMixin(TestCase):
    class TestForm(FormControlMixin, Form):
        name = CharField()
        status = CharField(widget=CheckboxInput())

    def test__form_control_class_added(self):
        form = self.TestForm()
        self.assertEquals(
            form.fields['name'].widget.attrs['class'],
            'form-control'
        )

        self.assertNotIn(
            'class',
            form.fields['status'].widget.attrs
        )
