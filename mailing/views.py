from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView, View
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.http import HttpResponseForbidden
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.views.decorators.vary import vary_on_cookie


from .models import Client, Message, Mailing, MailingAttempt
from .forms import ClientForm, MessageForm, MailingForm
from .services import send_mailing
from .mixins import OwnerOrManagerMixin
from users.mixins import BlockCheckMixin


class ClientListView(BlockCheckMixin, LoginRequiredMixin, ListView):
    model = Client
    template_name = 'mailing/client_list.html'
    context_object_name = 'clients'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Менеджеры').exists():
            return Client.objects.all()
        return Client.objects.filter(owner=user)


@method_decorator([cache_page(60 * 10), vary_on_cookie], name='dispatch')
class ClientDetailView(BlockCheckMixin, LoginRequiredMixin, DetailView):
    model = Client
    template_name = 'mailing/client_detail.html'
    context_object_name = 'client'

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Менеджеры').exists():
            return Client.objects.all()
        return Client.objects.filter(owner=user)


class ClientCreateView(BlockCheckMixin, LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'mailing/client_form.html'
    success_url = reverse_lazy('mailing:client_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ClientUpdateView(BlockCheckMixin, LoginRequiredMixin, OwnerOrManagerMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'mailing/client_form.html'

    def get_success_url(self):
        return reverse_lazy('mailing:client_detail', kwargs={'pk': self.object.pk})

    def get_queryset(self):
        return Client.objects.filter(owner=self.request.user)


class ClientDeleteView(BlockCheckMixin, LoginRequiredMixin, OwnerOrManagerMixin, DeleteView):
    model = Client
    template_name = 'mailing/client_confirm_delete.html'
    success_url = reverse_lazy('mailing:client_list')

    def get_queryset(self):
        return Client.objects.filter(owner=self.request.user)


class MessageListView(BlockCheckMixin, LoginRequiredMixin, ListView):
    model = Message
    template_name = 'mailing/message_list.html'
    context_object_name = 'messages'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Менеджеры').exists():
            return Message.objects.all()
        return Message.objects.filter(owner=user)


@method_decorator([cache_page(60 * 10), vary_on_cookie], name='dispatch')
class MessageDetailView(BlockCheckMixin, LoginRequiredMixin, DetailView):
    model = Message
    template_name = 'mailing/message_detail.html'
    context_object_name = 'message'

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Менеджеры').exists():
            return Message.objects.all()
        return Message.objects.filter(owner=user)


class MessageCreateView(BlockCheckMixin, LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:message_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(BlockCheckMixin, LoginRequiredMixin, OwnerOrManagerMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:message_list')

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)


class MessageDeleteView(BlockCheckMixin, LoginRequiredMixin, OwnerOrManagerMixin, DeleteView):
    model = Message
    template_name = 'mailing/message_confirm_delete.html'
    success_url = reverse_lazy('mailing:message_list')

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)


class MailingListView(BlockCheckMixin, LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'mailing/mailing_list.html'
    context_object_name = 'mailings'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Менеджеры').exists():
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=user)


@method_decorator([cache_page(60 * 10), vary_on_cookie], name='dispatch')
class MailingDetailView(BlockCheckMixin, LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = 'mailing/mailing_detail.html'
    context_object_name = 'mailing'

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Менеджеры').exists():
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        mailing = self.get_object()

        context['can_stop'] = (
                mailing.status != 'Завершена' and
                (mailing.owner == user or user.groups.filter(name='Менеджеры').exists())
        )
        return context


class MailingCreateView(BlockCheckMixin, LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailing_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user

        form.fields['message'].queryset = Message.objects.filter(owner=user)
        form.fields['clients'].queryset = Client.objects.filter(owner=user)
        return form

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.status = 'Создана'
        return super().form_valid(form)


class MailingUpdateView(BlockCheckMixin, LoginRequiredMixin, OwnerOrManagerMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailing_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user

        form.fields['message'].queryset = Message.objects.filter(owner=user)
        form.fields['clients'].queryset = Client.objects.filter(owner=user)
        return form


class MailingDeleteView(BlockCheckMixin, LoginRequiredMixin, OwnerOrManagerMixin, DeleteView):
    model = Mailing
    template_name = 'mailing/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing:mailing_list')

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)


class MailingAttemptListView(BlockCheckMixin, LoginRequiredMixin, ListView):
    model = MailingAttempt
    template_name = 'mailing/attempt_list.html'
    context_object_name = 'attempts'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Менеджеры').exists():
            return MailingAttempt.objects.select_related('mailing').order_by('-timestamp')
        return MailingAttempt.objects.filter(mailing__owner=user).select_related('mailing').order_by('-timestamp')


@method_decorator([cache_page(60 * 10), vary_on_cookie], name='dispatch')
class HomePageView(TemplateView):
    template_name = 'mailing/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        total_mailings = Mailing.objects.all()
        context['total_number'] = total_mailings.count()
        context['total_active'] = total_mailings.filter(status='Запущена').count()
        context['total_clients'] = Client.objects.count()

        if self.request.user.is_authenticated:
            user_mailings = total_mailings.filter(owner=self.request.user)
            context['user_mailings_number'] = user_mailings.count()
            context['user_active'] = user_mailings.filter(status='Запущена').count()
            context['user_clients'] = Client.objects.filter(owner=self.request.user).count()

        return context


class SendMailingView(BlockCheckMixin, LoginRequiredMixin, View):
    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk, owner=request.user)
        results = send_mailing(mailing)
        return render(request, 'mailing/send_result.html', {
            'mailing': mailing,
            'results': results
        })


@method_decorator([cache_page(60 * 10), vary_on_cookie], name='dispatch')
class MailingReportView(BlockCheckMixin, LoginRequiredMixin, TemplateView):
    template_name = 'mailing/report.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        attempts = MailingAttempt.objects.filter(mailing__owner=user)

        context['successful_attempts'] = attempts.filter(status='ok').count()
        context['failed_attempts'] = attempts.filter(status='fail').count()
        context['total_attempts'] = attempts.count()
        context['attempts'] = attempts.select_related('mailing')

        return context


class StopMailingView(BlockCheckMixin, LoginRequiredMixin, View):
    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        user = request.user

        if mailing.owner == user or user.groups.filter(name='Менеджеры').exists():
            mailing.status = 'Завершена'
            mailing.save()
            messages.success(request, 'Рассылка отключена')
            return redirect('mailing:mailing_detail', pk=pk)

        return HttpResponseForbidden('У вас нет прав отключить эту рассылку.')
