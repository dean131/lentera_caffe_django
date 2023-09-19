from django.contrib import admin

from .models import  Item, Kriteria, Subkriteria, Saw

# Register your models here.
admin.site.register(Item)
admin.site.register(Kriteria)
admin.site.register(Subkriteria)
admin.site.register(Saw)