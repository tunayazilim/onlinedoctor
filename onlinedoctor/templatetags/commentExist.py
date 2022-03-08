from onlinedoctor.models import CustomUserModel,CommentModel
from django.shortcuts import (get_object_or_404, render,
                              )
from django import template



register=template.Library()


@register.simple_tag
def isCommentExist(request,doctor):
    commmentExist=CommentModel.objects.filter(parent=None,is_published=True,doctor=doctor,comment_user=request.user).count()
    if commmentExist:
        return True
    else :
        return False