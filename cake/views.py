from django.shortcuts import render
from django import views


class BaseViews(views.View):
    def get(self, request, *args, **kwargs):
        title = 'Тортики'
        context = {'title': title}
        return render(request, 'base.html', context)


class OrderViews(views.View):
    def get(self, request, *args, **kwargs):
        title = 'Личный кабинет'
        context = {'title': title}
        return render(request, 'order.html', context)