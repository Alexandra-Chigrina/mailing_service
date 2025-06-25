from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    avatar = models.ImageField(upload_to="users/avatars/", verbose_name="Аватар", blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="Телефон")
    country = models.CharField(max_length=100, blank=True, null=True, verbose_name="Страна")
    is_blocked = models.BooleanField(default=False, verbose_name="Заблокирован")

    token = models.CharField(max_length=100, verbose_name="Token", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
