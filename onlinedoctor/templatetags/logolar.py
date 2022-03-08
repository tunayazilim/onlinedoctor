from onlinedoctor.models import logoModel
from django import template



register=template.Library()


@register.simple_tag
def logolars():
    logo=logoModel.objects.first()
    return logo