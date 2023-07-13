from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

UserModel = get_user_model()


@receiver(post_save, sender=UserModel)
def send_confirmation_email(sender, instance, created, **kwargs):
    if created:
        token = default_token_generator.make_token(instance)
        instance.confirmation_token = token
        instance.save()

        verification_url = reverse(
            'register-confirmation',
            kwargs={'token': token}
        )

        subject = 'Email Confirmation'
        message = f'Verify you email by clicking to the link below: {verification_url}'
        from_email = 'iveta.zhekova@gmail.com'
        recipient_list = ['iveta.zhekova@gmail.com']

        send_mail(subject, message, from_email, recipient_list)
