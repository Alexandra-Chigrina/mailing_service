from django.core.management.base import BaseCommand, CommandError

from mailing.models import Mailing
from mailing.services import send_mailing


class Command(BaseCommand):
    help = "Отправить рассылку вручную по её ID"

    def add_arguments(self, parser):
        parser.add_argument('mailing_id', type=int, help='ID рассылки')

    def handle(self, *args, **kwargs):
        mailing_id = kwargs['mailing_id']
        try:
            mailing = Mailing.objects.get(pk=mailing_id)
        except Mailing.DoesNotExist:
            raise CommandError(f'Рассылка с ID={mailing_id} не найдена.')

        self.stdout.write(f'Отправка рассылки #{mailing_id} началась...')
        results = send_mailing(mailing)
        self.stdout.write(self.style.SUCCESS('Отправка завершена.'))

        for result in results:
            self.stdout.write(f"- {result['client']}: {result['status']} — {result['response']}")
