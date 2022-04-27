from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    BaseViews, OrderViews,
    RegistrationView, LoginUserView
)


urlpatterns = [
    path('', BaseViews.as_view(), name='base'),
    path('order/', OrderViews.as_view(), name='order'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
]
