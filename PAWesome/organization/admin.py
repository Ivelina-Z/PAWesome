from django.contrib import admin

from PAWesome.organization.models import Organization, Employee


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not request.user.is_superuser:
            queryset = queryset.filter(pk=request.user.organization.pk)
        return queryset


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    search_fields = ('first_name', 'last_name')

    def has_add_permission(self, request):
        return request.user.is_superuser
