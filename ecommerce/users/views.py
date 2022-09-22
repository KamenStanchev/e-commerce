from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, views
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from ecommerce.store.models import Customer
from ecommerce.users.forms import NewUserForm


class UserRegister(generic.CreateView):
    form_class = NewUserForm
    template_name = 'register.html'
    success_url = reverse_lazy('store')

    def form_valid(self, form):
        messages.success(self.request, 'Account created successfully.')
        return super().form_valid(form)


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            customer, created = Customer.objects.get_or_create(user=user)
            messages.info(request, 'You successfully login.')
            return redirect('store')
        else:
            messages.error(request, f'User name: "{username}" or password is not correct.')

    return render(request, 'login.html')


class LogoutView(generic.View):
    def get(self, request):
        logout(request)
        messages.info(request, 'You successfully logout.')
        return redirect('store')
