from django import forms
from django.core.exceptions import ValidationError

from mailing.models import Client, Message, Mailing


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['email', 'full_name', 'comment']

    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Адрес электронной почты'})
        self.fields['full_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Фамилия Имя Отчество'})
        self.fields['comment'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Комментарий'})


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        self.fields['subject'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Тема сообщения'})
        self.fields['body'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Тело сообщения'})


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing  # ← правильно
        fields = ['start_time', 'end_time', 'message', 'clients', 'period']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control',
                'placeholder': 'ДД.ММ.ГГГГ ЧЧ:ММ'
            }, format='%Y-%m-%dT%H:%M'),
            'end_time': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control',
                'placeholder': 'ДД.ММ.ГГГГ ЧЧ:ММ'
            }, format='%Y-%m-%dT%H:%M'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Общие классы для остальных полей
        self.fields['message'].widget.attrs.update({'class': 'form-control'})
        self.fields['clients'].widget.attrs.update({'class': 'form-control'})
        self.fields['period'].widget.attrs.update({'class': 'form-control'})
