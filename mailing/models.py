from django.db import models

from users.models import CustomUser


class Client(models.Model):
    email = models.EmailField(unique=True, verbose_name='Email')
    full_name = models.CharField(max_length=255, verbose_name='ФИО')
    comment = models.TextField(verbose_name='Комментарий', blank=True, null=True)
    owner = models.ForeignKey(CustomUser, verbose_name="Владелец", on_delete=models.CASCADE, related_name='clients')

    class Meta:
        verbose_name = 'Получатель рассылки'
        verbose_name_plural = 'Получатели рассылки'
        ordering = ["full_name"]

    def __str__(self):
        return f'{self.full_name} <{self.email}>'


class Message(models.Model):
    subject = models.CharField(max_length=255, verbose_name='Тема письма')
    body = models.TextField(verbose_name='Тело письма')
    owner = models.ForeignKey(CustomUser, verbose_name="Владелец", on_delete=models.CASCADE, related_name='messages')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return self.subject


class Mailing(models.Model):
    STATUS_CHOICES = [
        ('Создана', 'Создана'),
        ('Запущена', 'Запущена'),
        ('Завершена', 'Завершена'),
    ]

    start_time = models.DateTimeField(verbose_name='Дата и время первой отправки')
    end_time = models.DateTimeField(verbose_name='Дата и время окончания отправки')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Создана',
                              verbose_name="Статус сообщения")
    message = models.ForeignKey(Message, verbose_name="Сообщение", on_delete=models.CASCADE, related_name='mailings')
    clients = models.ManyToManyField(Client, verbose_name='Получатели', related_name='mailings')
    owner = models.ForeignKey(CustomUser, verbose_name="Владелец", on_delete=models.CASCADE, related_name='mailings',
                              blank=True, null=True)

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

    def __str__(self):
        return f'Рассылка #{self.id} - {self.status}'


class MailingAttempt(models.Model):
    STATUS_CHOICES = [
        ('Успешно', 'Успешно'),
        ('Не успешно', 'Не успешно'),
    ]

    timestamp = models.DateTimeField(verbose_name='Дата и время попытки', auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name='Статус рассылки')
    server_response = models.TextField(verbose_name='Ответ почтового сервера')
    mailing = models.ForeignKey(Mailing, verbose_name='Рассылка',on_delete=models.CASCADE, related_name='attempts')

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылки'

    def __str__(self):
        return f'Рассылка от {self.timestamp} - {self.status}'
