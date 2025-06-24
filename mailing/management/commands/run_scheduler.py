import logging
from datetime import timedelta
from django.core.management.base import BaseCommand
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore, register_events
from django.utils import timezone
from django.conf import settings

from mailing.models import Mailing
from mailing.services import send_mailing

logger = logging.getLogger('mailing')


def send_scheduled_mailings():
    now = timezone.now()
    mailings = Mailing.objects.filter(status='Создана', start_time__lte=now, end_time__gte=now)

    for mailing in mailings:
        logger.info(f"Отправка рассылки {mailing.pk} пользователю {mailing.owner}")
        send_mailing(mailing)

        # Вычисляем интервал между start и end
        period_delta = mailing.end_time - mailing.start_time

        if mailing.period == 'daily':
            mailing.start_time += timedelta(days=1)
            mailing.end_time = mailing.start_time + period_delta
            mailing.status = 'Создана'

        elif mailing.period == 'weekly':
            mailing.start_time += timedelta(weeks=1)
            mailing.end_time = mailing.start_time + period_delta
            mailing.status = 'Создана'

        elif mailing.period == 'monthly':
            mailing.start_time += timedelta(days=30)
            mailing.end_time = mailing.start_time + period_delta
            mailing.status = 'Создана'

        else:  # 'none'
            mailing.status = 'Завершена'

        mailing.save()


def delete_old_job_executions(max_age=604_800):
    from django_apscheduler.models import DjangoJobExecution
    DjangoJobExecution.objects.delete_old_job_executions(max_age)



class Command(BaseCommand):
    help = "Запуск планировщика рассылок."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            send_scheduled_mailings,
            trigger=CronTrigger(minute='*/1'),
            id="send_scheduled_mailings",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Добавлена задача: send_scheduled_mailings")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(day_of_week="mon", hour="00", minute="00"),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Добавлена задача: delete_old_job_executions")

        register_events(scheduler)

        try:
            logger.info("Запуск планировщика...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Остановка планировщика...")
            scheduler.shutdown()
            logger.info("Планировщик остановлен.")
