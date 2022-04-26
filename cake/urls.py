from django.urls import path
from .views import (
    BaseViews,
)

urlpatterns = [
    path('', BaseViews.as_view(), name='base'),
]
