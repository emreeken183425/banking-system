from django.contrib import messages
from django.contrib.auth import login, logout
from rest_framework import viewsets
from django.views import View
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from rest_framework.views import APIView
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.views import LoginView
from django.shortcuts import HttpResponseRedirect,render,redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import generics, status
from rest_framework.response import Response
from .forms import UserRegistrationForm, UserAddressForm
from .models import BankAccountType, UserBankAccount, UserAddress, UserProfile
from .serializers import BankAccountTypeSerializer, UserBankAccountSerializer, UserSerializer,UserAddressSerializer, UserProfileSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class UserDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)



class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer



class UserRegistrationView(TemplateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/user_registration.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('transactions:transaction_report'))
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        registration_form = UserRegistrationForm(self.request.POST)
        address_form = UserAddressForm(self.request.POST)

        if registration_form.is_valid() and address_form.is_valid():
           user = registration_form.save()
           address = address_form.save(commit=False)
           address.user = user
           address.save()

           user_bank_account = UserBankAccount.objects.get(user=user) 
           messages.success(
              self.request,
                f'Thank You For Creating A Bank Account. Your Account Number is {user_bank_account.account_no}.'
            )
           return HttpResponseRedirect(reverse_lazy('transactions:deposit_money'))


        return self.render_to_response(
            self.get_context_data(
                registration_form=registration_form,
                address_form=address_form
            )
        )

    def get_context_data(self, **kwargs):
        if 'registration_form' not in kwargs:
            kwargs['registration_form'] = UserRegistrationForm()
        if 'address_form' not in kwargs:
            kwargs['address_form'] = UserAddressForm()
        return super().get_context_data(**kwargs)


class UserLoginView(LoginView):
    template_name = 'accounts/user_login.html'
    redirect_authenticated_user = False


class LogoutView(RedirectView):
    pattern_name = 'home'

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            logout(self.request)
        return super().get_redirect_url(*args, **kwargs)


class BankAccountTypeListCreateView(generics.ListCreateAPIView):
    queryset = BankAccountType.objects.all()
    serializer_class = BankAccountTypeSerializer


class BankAccountTypeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BankAccountType.objects.all()
    serializer_class = BankAccountTypeSerializer


class UserBankAccountListCreateView(LoginRequiredMixin, generics.ListCreateAPIView):
    model = UserBankAccount
    serializer_class = UserBankAccountSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        account_types = BankAccountType.objects.all()
        context = {
            'account_types': account_types
        }
        return render(request, 'accounts/create_account.html', context=context)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserBankAccountRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserBankAccount.objects.all()
    serializer_class = UserBankAccountSerializer
    
class UserAddressViewSet(viewsets.ModelViewSet):
    queryset = UserAddress.objects.all()
    serializer_class = UserAddressSerializer



class AccountSettingsView(TemplateView):
    template_name = 'accounts/account_settings.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['account_types'] = BankAccountType.objects.all()
        context['user'] = User.objects.get(pk=self.request.user.pk)
        return context

    def post(self, request, *args, **kwargs):
        user = request.user
        account = user.account
        if 'update' in request.POST:
            account_type_name = request.POST.get('account_type')
            account_type = BankAccountType.objects.get(name=account_type_name)
            account.account_type = account_type

            account_no = request.POST.get('account_no')
            gender = request.POST.get('gender')
            birth_date = request.POST.get('birth_date')
            balance = request.POST.get('balance')
            interest_start_date = request.POST.get('interest_start_date')
            initial_deposit_date = request.POST.get('initial_deposit_date')
            account.account_type = account_type
            account.account_no = account_no
            account.gender = gender
            account.birth_date = birth_date
            account.balance = balance
            account.interest_start_date = interest_start_date
            account.initial_deposit_date = initial_deposit_date
            account.save()
            messages.success(request, 'Your account has been updated.')
            return redirect('accounts:account_settings')
        elif 'delete' in request.POST:
            account.delete()
            messages.success(request, 'Your account has been deleted.')
            return redirect('accounts:user_login')

   

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class UserProfileView(View):
    template_name = 'accounts/profile_settings.html'
    
    def get(self, request):
        return render(request, self.template_name)
    
    def profile_settings(self, request):
        user = request.user
        profile = user.profile
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.save()
        context = {
            'user': user,
            'profile': profile,
        }
        return render(request, 'accounts/profile_settings.html', context)

class UserProfileDetailView(APIView):

    def get_object(self, pk):
        try:
            return UserProfile.objects.get(user=pk)
        except UserProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        profile = self.get_object(pk)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request, pk):
        profile = self.get_object(pk)
        serializer = UserProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        profile = self.get_object(pk)
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





class DeleteAccountView(View):
    def delete(self, request, *args, **kwargs):
        # burada hesap silme işlemleri yapılabilir
        return redirect('home')

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    fields = ['first_name', 'last_name', 'address', 'bank_account']
    template_name = 'accounts/profile_settings.html'

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_success_url(self):
        return reverse_lazy('home')

    def form_valid(self, form):
        messages.success(self.request, 'Your profile has been updated.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'An error occurred while updating your profile.')
        return super().form_invalid(form)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    

