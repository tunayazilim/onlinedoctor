from onlinedoctor.models import  TimeScheduleModel
from django.shortcuts import (get_object_or_404, render,
                              )
from django import template



register=template.Library()


@register.simple_tag
def count_of_waiting_appointments(request):
    return TimeScheduleModel.objects.filter(doctor=request.user,is_paid="yes",status="pending").count()


