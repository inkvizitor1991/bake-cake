from django import views
from django.http import HttpResponseRedirect
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse

from .forms import RegisterUserForm, LoginUserForm


class BaseViews(views.View):

    def get(self, request, *args, **kwargs):
        title = 'Тортики'
        context = {
            'title': title
        }
        return render(request, 'base.html', context)


class OrderViews(views.View):

    def get(self, request, *args, **kwargs):
        title = 'Личный кабинет'
        context = {'title': title}
        return render(request, 'order.html', context)


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
        return reverse_lazy('order')
