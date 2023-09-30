from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(CustomUser)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(Checkout)
admin.site.register(Order)