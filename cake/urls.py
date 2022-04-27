from django.urls import path
from .views import (
    BaseViews, OrderViews
)

urlpatterns = [
    path('', BaseViews.as_view(), name='base'),
    path('order/', OrderViews.as_view(), name='order')
]
