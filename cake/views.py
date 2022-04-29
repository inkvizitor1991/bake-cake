import os
import uuid
import time
import threading
import json
import datetime

from yookassa import Configuration, Payment
from dotenv import load_dotenv

from django import views

from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from annoying.functions import get_object_or_None

from .forms import RegisterUserForm, LoginUserForm
from .models import Levels, Form, Topping, Berries, Decor, Cake, Client, Delivery, Order

load_dotenv()

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
            'user': user.first_name,
            'email': user.email,
            'client': client,
        }
        if client:
            context = {
                'title': title,
                'user': user.first_name,
                'email': user.email,
                'client': client,
                'orders': client.orders.all()
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


def show_index_page(request):
    levels = Levels.objects.all()
    forms = Form.objects.all()
    toppings = Topping.objects.all()
    berries = Berries.objects.all()
    decors = Decor.objects.all()

    cake_components_serialized = {
        'levels': {
            'quantity': [level.quantity for level in levels],
            'prices': [level.price for level in levels]
        },
        'forms': {
            'figures': [form.figure for form in forms],
            'prices': [form.price for form in forms]
        },
        'toppings': {
            'names': [topping.name for topping in toppings],
            'prices': [topping.price for topping in toppings]
        },
        'berries': {
            'names': [berry.name for berry in berries],
            'prices': [berry.price for berry in berries]
        },
        'decors': {
            'names': [decor.name for decor in decors],
            'prices': [decor.price for decor in decors]
        }
    }

    return render(request, 'index.html', context={
        'cake_components': cake_components_serialized
    })



def check_payment_until_confirm(payment_id, subscription_uuid):
    while True:
        payment = Payment.find_one(payment_id)
        if payment.status == "canceled":
            print('Не успешная оплата')
            return
        if payment.status == "succeeded":
            print('Успешная оплата, сохраним данные')
            return

        time.sleep(5)


def payment(request):
    Configuration.account_id = os.getenv('YOOKASSA_ACCOUNT_ID')
    Configuration.secret_key = os.getenv('YOOKASSA_SECRET_KEY')
    subscription_uuid = uuid.uuid4()
    payment = Payment.create({
        "amount": {
            "value": "100.00",
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": request.build_absolute_uri(reverse('account'))
        },
        "capture": True,
        "description": "Заказ №1"
    })

    threading.Thread(
        target=check_payment_until_confirm,
        args=[payment.id, subscription_uuid],
        daemon=True
    ).start()
    return redirect(payment.confirmation.confirmation_url)


def pass_cake_ingridients(request):
    levels = Levels.objects.all()
    forms = Form.objects.all()
    toppings = Topping.objects.all()
    berries = Berries.objects.all()
    decors = Decor.objects.all()

    cake_components_serialized = {
        'levels': {
            'quantity': [level.quantity for level in levels],
            'prices': [level.price for level in levels]
        },
        'forms': {
            'figures': [form.figure for form in forms],
            'prices': [form.price for form in forms]
        },
        'toppings': {
            'names': [topping.name for topping in toppings],
            'prices': [topping.price for topping in toppings]
        },
        'berries': {
            'names': [berry.name for berry in berries],
            'prices': [berry.price for berry in berries]
        },
        'decors': {
            'names': [decor.name for decor in decors],
            'prices': [decor.price for decor in decors]
        }
    }

    response = JsonResponse(
        cake_components_serialized,
        json_dumps_params={'ensure_ascii': False, 'indent': 4}
    )

    return response


def register_order(request):
    try:
        order_raw = json.loads(request.body.decode())
        print(order_raw)

        levels = Levels.objects.get(quantity=order_raw['Levels'])
        form = Form.objects.get(figure=order_raw['Form'])
        topping = Topping.objects.get(name=order_raw['Topping'])
        berries = Berries.objects.get(name=order_raw['Berries'])
        decor = Decor.objects.get(name=order_raw['Decor'])

        cake = Cake.objects.create(
            levels=levels,
            form=form,
            topping=topping,
            berries=berries,
            decor=decor,
            words=order_raw['Words'],
        )

        username = str(uuid.uuid4())
        first_name = order_raw['Name']
        client_email = order_raw['Email']
        password = User.objects.make_random_password()

        user = User.objects.create_user(
            username,
            client_email,
            password,
            first_name=first_name
        )

        client = Client.objects.create(
            user=user,
            phone=order_raw['Phone']
        )

        year, month, day = order_raw['Dates'].split('-')
        hours, minutes = order_raw['Time'].split(':')
        deliver_datetime = datetime.datetime(
            int(year),
            int(month),
            int(day),
            int(hours),
            int(minutes)
        )

        delivery = Delivery.objects.create(
            address=order_raw['Address'],
            deliver_at=deliver_datetime,
            comment=order_raw['DelivComments']
        )

        order = Order.objects.create(
            client=client,
            cake=cake,
            price=order_raw['Cost'],
            delivery=delivery,
            comment=order_raw['Comments']
        )

        login(request, user)

        return JsonResponse({
            'order': order_raw,
            'status': 'ok'
        })

    except ValueError:
        return JsonResponse({
            'status': 'error',
            'error': 'Order not created',
        })
