import secrets

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetView
from django.core.mail import send_mail
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, View

from config.settings import EMAIL_HOST_USER
from users.forms import CustomUserCreationForm, ProfileUpdateForm
from users.models import CustomUser


class RegisterView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/email_confirm/{token}/"

        message = (
            f"Здравствуйте!\n\n"
            f"Спасибо за регистрацию на нашем сайте.\n"
            f"Пожалуйста, подтвердите ваш адрес электронной почты, перейдя по ссылке:\n\n{url}\n\n"
            f"Если вы не регистрировались, просто проигнорируйте это письмо.\n\nС уважением, команда сайта."
        )

        send_mail(
            subject="Подтверждение почты",
            message=message,
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )

        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(CustomUser, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = ProfileUpdateForm
    template_name = "users/profile_edit.html"
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return self.request.user


class ProfileListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = CustomUser
    template_name = "users/profile_list.html"
    context_object_name = "users"
    paginate_by = 10

    def test_func(self):
        return self.request.user.groups.filter(name="Менеджеры").exists()


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = "users/profile_detail.html"
    context_object_name = "user_profile"

    def get_object(self, queryset=None):
        return self.request.user


class CustomPasswordResetView(PasswordResetView):
    email_template_name = "users/password_reset_email.html"
    success_url = reverse_lazy("users:password_reset_done")


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "users/password_reset_confirm.html"
    success_url = reverse_lazy("users:password_reset_complete")


class BlockUserView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.groups.filter(name="Менеджеры").exists()

    def post(self, request, pk):
        user_to_toggle = get_object_or_404(CustomUser, pk=pk)

        if user_to_toggle == request.user:
            return HttpResponseForbidden("Вы не можете заблокировать самого себя.")

        if user_to_toggle.is_superuser:
            return HttpResponseForbidden("Нельзя блокировать суперпользователя.")

        user_to_toggle.is_blocked = not user_to_toggle.is_blocked
        user_to_toggle.save()

        if user_to_toggle.is_blocked:
            messages.success(request, f"Пользователь {user_to_toggle.email} успешно заблокирован.")
        else:
            messages.success(request, f"Пользователь {user_to_toggle.email} снова активен.")

        return redirect("users:profile_list")
