class FormControlMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field_value in self.fields.items():
            self.fields[field_name].widget.attrs['class'] = 'form-control'
