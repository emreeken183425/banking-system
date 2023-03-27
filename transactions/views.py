from dateutil.relativedelta import relativedelta
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, ListView

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
        queryset = super().get_queryset().filter(account=self.request.user.account)
        daterange = self.form_data.get("daterange")
        min_amount = self.form_data.get("min_amount")
        max_amount = self.form_data.get("max_amount")

        # Filtreleme parametrelerine göre sorguyu güncelle
        if daterange:
            queryset = queryset.filter(timestamp__date__range=daterange)

        if min_amount and max_amount:
            queryset = queryset.filter(amount__range=[Decimal(min_amount), Decimal(max_amount)])
        elif min_amount:
            queryset = queryset.filter(amount__gte=Decimal(min_amount))
        elif max_amount:
            queryset = queryset.filter(amount__lte=Decimal(max_amount))

        transaction_type = self.request.GET.get('transaction_type')
        if transaction_type:
            queryset = queryset.filter(transaction_type=transaction_type)

        return queryset.order_by('-timestamp')

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
            next_interest_month = int(
                12 / account.account_type.interest_calculation_per_year
            )
            account.initial_deposit_date = now
            account.interest_start_date = (
                now + relativedelta(
                    months=+next_interest_month
                )
            )

        account.balance += amount
        account.save(
            update_fields=[
                'initial_deposit_date',
                'balance',
                'interest_start_date'
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
