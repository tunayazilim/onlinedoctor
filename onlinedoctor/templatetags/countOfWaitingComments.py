from onlinedoctor.models import CustomUserModel,CommentModel
from django.shortcuts import (get_object_or_404, render,
                              )
from django import template



register=template.Library()


@register.simple_tag
def count_of_waiting_comments():
    return CommentModel.objects.filter(is_published=False).count()


