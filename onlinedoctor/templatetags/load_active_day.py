from onlinedoctor.models import CustomUserModel
from django.shortcuts import (get_object_or_404, render,
                              )
from django import template



register=template.Library()


@register.simple_tag
def load_active_day_of(request):
    nav_obj = get_object_or_404(CustomUserModel,email=request.user.email)
   # print(nav_obj.active_day+" loaddan")
    return nav_obj


