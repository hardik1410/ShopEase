from core.models import Owner
from django.contrib import admin
from .models import Owner, Store

# Register your models here.

admin.site.register(Owner)
admin.site.register(Store)