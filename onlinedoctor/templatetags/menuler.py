from onlinedoctor.models import CustomUserModel
from Admin.models import topMenuModel
from django.shortcuts import (get_object_or_404, render,
                              )
from django import template



register=template.Library()


@register.simple_tag
def get_menuler(request):
    if request.user.is_authenticated:
        if request.user.is_patient:
            return topMenuModel.objects.filter(userType="patient").order_by("menuSira")
        if request.user.is_doctor:
            return topMenuModel.objects.filter(userType="doctor").order_by("menuSira")
    else:
        return topMenuModel.objects.filter(userType="nouser").order_by("menuSira")

