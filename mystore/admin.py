from django.contrib import admin

from .models import *

admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Comment)
admin.site.register(Category)
