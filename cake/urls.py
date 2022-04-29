from django.urls import path
from django.contrib.auth.views import LogoutView
from cake import views
from .views import (
    BaseViews, AccountViews,
    RegistrationView, LoginUserView
)

urlpatterns = [
    path('', BaseViews.as_view(), name='base'),
    path('account/', AccountViews.as_view(), name='account'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),

    path('cake/', views.show_index_page, name="indexpage"),
    path('api/order/', views.register_order, name="api_order"),
]
