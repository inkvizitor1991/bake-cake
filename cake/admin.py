from django.contrib import admin

from .models import Levels, Form, Topping, Berries, Decor
from .models import Cake
from .models import Client
from .models import Delivery
from .models import Order


admin.site.register(Levels)
admin.site.register(Form)
admin.site.register(Topping)
admin.site.register(Berries)
admin.site.register(Decor)
admin.site.register(Cake)
admin.site.register(Client)
admin.site.register(Delivery)
admin.site.register(Order)
