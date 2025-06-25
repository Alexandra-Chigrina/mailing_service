from django.core.mail import send_mail
from django.utils import timezone
import logging

from config.settings import EMAIL_HOST_USER
from .models import MailingAttempt


logger = logging.getLogger('mailing')

def send_mailing(mailing):
    logger.info(f"Начата рассылка ID={mailing.pk} пользователю {mailing.owner}")
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
                status='ok',
                server_response='Отправлено успешно',
                timestamp=timezone.now()
            )

            logger.info(f"Успешно отправлено письмо клиенту {client.email} для рассылки ID={mailing.pk}")

            results.append({
                'client': client,
                'status': 'ok',
                'response': 'Отправлено успешно'
            })

        except Exception as e:
            MailingAttempt.objects.create(
                mailing=mailing,
                status='fail',
                server_response=str(e),
                timestamp=timezone.now()
            )

            logger.error(f"Ошибка при отправке письма клиенту {client.email} (рассылка ID={mailing.pk}): {e}")

            results.append({
                'client': client,
                'status': 'fail',
                'response': str(e)
            })

    if mailing.period == 'none':
        mailing.status = 'Завершена'
    else:
        mailing.status = 'Создана'
    mailing.save()

    logger.info(f"Завершена рассылка ID={mailing.pk} пользователю {mailing.owner}")

    return results