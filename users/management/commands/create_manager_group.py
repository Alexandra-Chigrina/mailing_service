from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Создает группу менеджеры и назначает права"

    def handle(self, *args, **kwargs):
        group, created = Group.objects.get_or_create(name="Менеджеры")

        permissions = Permission.objects.filter(
            codename__in=[
                "view_all_mailings",
                "deactivate_mailing",
                "view_all_clients",
                "view_all_messages",
            ]
        )
        group.permissions.set(permissions)
        group.save()

        self.stdout.write(self.style.SUCCESS('Группа "Менеджеры" создана и права назначены.'))
