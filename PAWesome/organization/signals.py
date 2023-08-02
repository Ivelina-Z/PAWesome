from django.core.mail import send_mail
from django.db.models.signals import post_delete
from django.dispatch import receiver

from PAWesome import settings
from PAWesome.adoption.models import SubmittedAdoptionSurvey


@receiver(post_delete, sender=SubmittedAdoptionSurvey)
def send_rejection_mail(sender, instance, **kwargs):
    if instance.status == 'rejected':
        subject = f'Отказ за осиновяване на {instance.animal}'
        message = f'Организацията отказа вашето искане за осиновяване.'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [instance.email]

        send_mail(subject, message, from_email, recipient_list)

