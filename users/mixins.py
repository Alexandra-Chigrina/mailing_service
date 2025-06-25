from django.http import HttpResponseForbidden


class BlockCheckMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_blocked:
            return HttpResponseForbidden("Ваш аккаунт заблокирован.")
        return super().dispatch(request, *args, **kwargs)
