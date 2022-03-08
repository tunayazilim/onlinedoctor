from onlinedoctor.models import footerModel
from django import template



register=template.Library()


@register.simple_tag
def footerPart():
    footer=footerModel.objects.first()
    return footer