from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse

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
            'edit_url': edit_url,
            'delete_url': delete_url
        }

        from_email = 'iveta.zhekova@gmail.com'
        # recipient_list = ['iveta.zhekova@gmail.com']

        message_body = render_to_string('foster_home/foster-home-email.html', context)
        send_mail(
            subject='',
            message=' ',
            html_message=message_body,
            from_email=from_email,
            recipient_list=[instance.email]
        )
