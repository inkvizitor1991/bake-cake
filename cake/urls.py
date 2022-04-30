from django.urls import path
from django.contrib.auth.views import LogoutView

from cake import views
from .views import (
    AccountViews
)

urlpatterns = [
    path('', views.show_index_page, name='indexpage'),
    path('account/', AccountViews.as_view(), name='account'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('payment/', views.payment, name='payment'),
    path('cake_ingridients/', views.pass_cake_ingridients, name="cake_ingridients"),
    path('api/order/', views.register_order, name="api_order"),
]
