from django.core.mail import send_mail
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from .models import MailingAttempt


def send_mailing(mailing):
    mailing.status = 'Запущена'
    mailing.save()

    results = []

    for client in mailing.clients.all():
        try:
            send_mail(
                subject=mailing.message.subject,
                message=mailing.message.body,
                from_email=EMAIL_HOST_USER,
                recipient_list=[client.email],
                fail_silently=False,
            )

            MailingAttempt.objects.create(
                mailing=mailing,
                status='успешно',
                server_response='Отправлено успешно',
                timestamp=timezone.now()
            )

            results.append({
                'client': client,
                'status': 'успешно',
                'response': 'Отправлено успешно'
            })

        except Exception as e:
            MailingAttempt.objects.create(
                mailing=mailing,
                status='ошибка',
                server_response=str(e),
                timestamp=timezone.now()
            )

            results.append({
                'client': client,
                'status': 'ошибка',
                'response': str(e)
            })

    mailing.status = 'Завершена'
    mailing.save()

    return results