from django.apps import AppConfig


class AuthAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'PAWesome.auth_app'

    def ready(self):
        import PAWesome.auth_app.signals
