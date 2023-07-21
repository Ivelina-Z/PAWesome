from django.forms import CheckboxInput


class FormControlMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field_value in self.fields.items():
            if not isinstance(self.fields[field_name].widget, CheckboxInput):
                self.fields[field_name].widget.attrs['class'] = 'form-control'


class OrganizationMixin:
    """
        Returns the associated organization object with the Organization or Employee user.
    """
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def get_organization(self):
        if self.request.user.groups.filter(name='Organizations').exists():
            return self.request.user.organization
        elif self.request.user.groups.filter(name='Employees').exists():
            return self.request.user.employee.organization

    def get_employee(self):
        if self.request.user.groups.filter(name='Employees').exists():
            return self.request.user.employee

    def is_organization(self):
        if self.request.user.groups.filter(name='Organizations').exists():
            return True

    def is_employee(self):
        if self.request.user.groups.filter(name='Employees').exists():
            return True
