from dateutil.relativedelta import relativedelta

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, ListView
import datetime
from transactions.constants import DEPOSIT, WITHDRAWAL
from transactions.forms import (
    DepositForm,
    TransactionDateRangeForm,
    WithdrawForm,
)
from transactions.models import Transaction


class TransactionRepostView(LoginRequiredMixin, ListView):
    template_name = 'transactions/transaction_report.html'
    model = Transaction
    form_data = {}

    def get(self, request, *args, **kwargs):
        form = TransactionDateRangeForm(request.GET or None)
        if form.is_valid():
            self.form_data = form.cleaned_data

        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        filter_type = self.request.GET.get('filter')
        queryset = queryset.filter(account__user=self.request.user)
        if filter_type == 'date':
           daterange = self.request.GET.get('daterange')
           if daterange:
            dates = daterange.split(" - ")
            if len(dates) == 2:
                start_date = datetime.datetime.strptime(dates[0], '%Y-%m-%d').date()
                end_date = datetime.datetime.strptime(dates[1], '%Y-%m-%d').date() + datetime.timedelta(days=1)
                queryset = queryset.filter(timestamp__range=[start_date, end_date], account__user=self.request.user)
            else:
                messages.warning(self.request, "Please enter a valid date range.")
        elif filter_type == 'deposit':
          queryset = queryset.filter(transaction_type=1, account__user=self.request.user)
        elif filter_type == 'withdraw':
          queryset = queryset.filter(transaction_type=2, account__user=self.request.user)
        elif filter_type == 'amount':
            queryset = queryset.filter(transaction_type=3, account__user=self.request.user, amount__lt=0)
        else:
          queryset = queryset.filter(account__user=self.request.user)
        return queryset



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        account = self.request.user.account
        transactions = context['object_list']
        final_balance = account.balance
        for transaction in transactions:
            if transaction.transaction_type == DEPOSIT:
                final_balance += transaction.amount
            elif transaction.transaction_type == WITHDRAWAL:
                final_balance -= transaction.amount

            transaction.balance_after_transaction = final_balance

        context['account'] = account
        context['final_balance'] = final_balance
        context['form'] = TransactionDateRangeForm(initial=self.form_data)
        return context


class TransactionCreateMixin(LoginRequiredMixin, CreateView):
    template_name = 'transactions/transaction_form.html'
    model = Transaction
    title = ''
    success_url = reverse_lazy('transactions:transaction_report')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'account': self.request.user.account
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title
        })

        return context


class DepositMoneyView(TransactionCreateMixin):
    form_class = DepositForm
    title = 'Deposit Money to Your Account'

    def get_initial(self):
        initial = {'transaction_type': DEPOSIT}
        return initial

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.account

        if not account.initial_deposit_date:
            now = timezone.now()
            
            account.initial_deposit_date = now
            

        account.balance += amount
        account.save(
            update_fields=[
                'initial_deposit_date',
                'balance',
               
            ]
        )

        messages.success(
            self.request,
            f'{amount}$ was deposited to your account successfully'
        )

        return super().form_valid(form)


class WithdrawMoneyView(TransactionCreateMixin):
    form_class = WithdrawForm
    title = 'Withdraw Money from Your Account'

    def get_initial(self):
        initial = {'transaction_type': WITHDRAWAL}
        return initial

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')

        self.request.user.account.balance -= form.cleaned_data.get('amount')
        self.request.user.account.save(update_fields=['balance'])

        messages.success(
            self.request,
            f'Successfully withdrawn {amount}$ from your account'
        )

        return super().form_valid(form)
