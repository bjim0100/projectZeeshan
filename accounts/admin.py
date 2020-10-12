from django.contrib import admin

from accounts.models import *

admin.site.register(Customer)
admin.site.register(Products)
admin.site.register(Order)
admin.site.register(Tag)

# Register your models here.
