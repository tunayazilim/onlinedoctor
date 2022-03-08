from django.contrib import admin
from .models import TimeScheduleModel, bannerModel,alanModel,alanYazilarModel,CustomUserModel,CommentModel
# Register your models here.


admin.site.register(bannerModel)
admin.site.register(alanModel)
admin.site.register(alanYazilarModel)
admin.site.register(CustomUserModel)
admin.site.register(CommentModel)
admin.site.register(TimeScheduleModel)