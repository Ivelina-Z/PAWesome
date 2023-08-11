from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy

from PAWesome import settings

UserModel = get_user_model()


@receiver(post_save, sender=UserModel)
def send_confirmation_email(sender, instance, created, **kwargs):
    if created:
        token = default_token_generator.make_token(instance)
        instance.confirmation_token = token
        instance.save()

        context = (
            {'confirmation_url': f"http://{settings.ALLOWED_HOSTS[0]}:8000/{(reverse('register-confirmation', kwargs={'token': token}))}"}
        )

        from_email = settings.EMAIL_HOST_USER

        message_body = render_to_string('email-verification.html', context)

        send_mail(
            subject='Email Confirmation',
            message=' ',
            html_message=message_body,
            from_email=from_email,
            recipient_list=[instance.email]
        )
