from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseForbidden


class OwnerOrManagerMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        user = self.request.user

        if user.groups.filter(name='Менеджеры').exists():
            return obj.owner == user

        return obj.owner == user

    def handle_no_permission(self):
        return HttpResponseForbidden('У вас нет прав для редактирования этого объекта.')
