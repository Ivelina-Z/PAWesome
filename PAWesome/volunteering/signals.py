from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse

from PAWesome import settings
from PAWesome.volunteering.models import FosterHome
from PAWesome.volunteering.token import Token


@receiver(post_save, sender=FosterHome)
def send_email(sender, instance, created, **kwargs):
    if created:
        token = Token().get_token()
        instance.token = token
        instance.save()

        edit_url = reverse(
            'foster-home-edit',
            kwargs={'token': token}
        )

        delete_url = reverse(
            'foster-home-delete',
            kwargs={'token': token}
        )

        context = {
            'subject': 'Потвърджение на заявка за приемен дом',
            'edit_url': f"http://{settings.ALLOWED_HOSTS[0]}:8000/{reverse('foster-home-edit', kwargs={'token': token})}",
            'delete_url': f"http://{settings.ALLOWED_HOSTS[0]}:8000/{(reverse('foster-home-delete', kwargs={'token': token}))}"
        }

        from_email = settings.EMAIL_HOST_USER

        message_body = render_to_string('foster_home/email-foster-home.html', context)
        send_mail(
            subject='Потвърждение за записване за приемен дом',
            message=' ',
            html_message=message_body,
            from_email=from_email,
            recipient_list=[instance.email]
        )
