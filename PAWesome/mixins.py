from django.forms import CheckboxInput


class FormControlMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field_value in self.fields.items():
            if not isinstance(self.fields[field_name].widget, CheckboxInput):
                self.fields[field_name].widget.attrs['class'] = 'form-control'

