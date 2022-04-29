from django import views

from django.http import HttpResponseRedirect
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from annoying.functions import get_object_or_None

from .forms import RegisterUserForm, LoginUserForm
from .models import Client, Order


class BaseViews(views.View):

    def get(self, request, *args, **kwargs):
        title = 'Тортики'
        context = {
            'title': title
        }
        return render(request, 'base.html', context)


class AccountViews(views.View):

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=request.user)
        client = get_object_or_None(Client, user__username=str(user))
        title = 'Личный кабинет'
        context = {
            'title': title,
            'user': user,
            'email': user.email,
            'client': client,
        }
        if client:
            context = {
                'title': title,
                'user': user,
                'email': user.email,
                'client': client,
                'phone': client,
                'id': client.order.cake.id,
                'levels': client.order.cake.levels.quantity,
                'form': client.order.cake.form,
                'topping': client.order.cake.topping,
                'berries': client.order.cake.berries,
                'decor': client.order.cake.decor,
                'words': client.order.cake.words,
                'price': client.order.price,
                'delivery': client.order.delivery.deliver_at,
            }

        return render(request, 'account.html', context)


class RegistrationView(CreateView):
    form_class = RegisterUserForm
    template_name = 'registration.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('base')


class LoginUserView(LoginView):
    form_class = LoginUserForm
    template_name = 'login.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'
        return context

    def get_success_url(self):
        return reverse_lazy('account')
