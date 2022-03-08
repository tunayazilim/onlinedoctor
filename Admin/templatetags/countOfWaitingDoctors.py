from onlinedoctor.models import CustomUserModel
from django import template



register=template.Library()


@register.simple_tag
def count_of_waiting_doctors():
    return CustomUserModel.objects.filter(is_doctor=True,doctor_okey=False).count()


