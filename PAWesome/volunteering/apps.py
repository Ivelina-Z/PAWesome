from django.apps import AppConfig


class VolunteeringConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "PAWesome.volunteering"

    def ready(self):
        from PAWesome.volunteering import signals
