from django.contrib import admin
from .models import bottomMenuModel, topMenuModel
# Register your models here.



admin.site.register(topMenuModel)
admin.site.register(bottomMenuModel)