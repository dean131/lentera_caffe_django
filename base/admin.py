from django.contrib import admin

from .models import  Item, Kriteria, Subkriteria, Saw, Order, OrderItem

# Register your models here.
admin.site.register(Item)
admin.site.register(Kriteria)
admin.site.register(Subkriteria)
admin.site.register(Saw)
admin.site.register(Order)
admin.site.register(OrderItem)