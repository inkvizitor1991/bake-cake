from django.shortcuts import render
from django import views


class BaseViews(views.View):
    def get(self, request, *args, **kwargs):
        title = 'Магазин для заказа тортов'
        context = {'title': title}
        return render(request, 'base.html', context)