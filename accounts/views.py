from django.contrib import messages
from django.contrib.auth import login, logout
from rest_framework import viewsets
from django.views import View
from rest_framework.views import APIView
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.views import LoginView
from django.shortcuts import HttpResponseRedirect,render
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



class AccountSettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/account_settings.html'
   

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class UserProfileView(View):
    template_name = 'accounts/profile_settings.html'
    
    def get(self, request):
        return render(request, self.template_name)


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


def profile_settings(request):
    user = request.user
    profile = user.profile
    context = {
        'user': user,
        'profile': profile,
    }
    return render(request, 'profile_settings.html', context)