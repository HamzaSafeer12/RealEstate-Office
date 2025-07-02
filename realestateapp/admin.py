from django.contrib import admin

# Register your models here.
from .models import PropertyType, SubPropertyType, Property

admin.site.register(PropertyType)
admin.site.register(SubPropertyType)
admin.site.register(Property)