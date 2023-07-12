class OrganizationMixin:
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def get_organization(self):
        if self.request.user.groups.filter(name='Organizations').exists():
            return self.request.user.organization
        elif self.request.user.groups.filter(name='Employees').exists():
            return self.request.user.employee.organization
        return None
