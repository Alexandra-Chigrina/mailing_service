from django.contrib import admin
from .models import Client, Message, Mailing, MailingAttempt


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'owner')
    list_filter = ('owner',)
    search_fields = ('full_name', 'email')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'owner')
    list_filter = ('owner',)
    search_fields = ('subject',)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'start_time', 'end_time', 'owner')
    list_filter = ('status', 'start_time', 'end_time', 'owner')
    date_hierarchy = 'start_time'
    filter_horizontal = ('clients',)
    search_fields = ('message__subject',)


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'status', 'mailing')
    list_filter = ('status', 'timestamp')
    search_fields = ('server_response',)
