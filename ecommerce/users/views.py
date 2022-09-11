from django.contrib.auth import authenticate, login, forms
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import View


from ecommerce.users.forms import NewUserForm


class UserRegister(generic.CreateView):
    form_class = NewUserForm
    template_name = 'register.html'
    success_url = reverse_lazy('store')


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('store')

    return render(request, 'login.html')
