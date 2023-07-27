from django.apps import AppConfig


class OrganizationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "PAWesome.organization"

    def ready(self):
        import PAWesome.organization.signals
