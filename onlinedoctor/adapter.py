import json
import base64
import logging

from django.core.exceptions import FieldDoesNotExist
from django.db.models import  FileField
from django.db.models.fields import (BinaryField)
from django.utils import six
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import HttpResponse, redirect

try:
    from django.utils.encoding import force_text
except ImportError:
    from django.utils.encoding import force_unicode as force_text

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import DefaultAccountAdapter
from allauth.utils import SERIALIZED_DB_FIELD_PREFIX
from allauth.exceptions import ImmediateHttpResponse



from onlinedoctor.models import CustomUserModel
logger = logging.getLogger("django")





def my_serialize_instance(instance):
    """Instance serializer supported of serialization of TimeZoneField.
    :param instance:
    :return:
    """
    data = {}
    for k, v in instance.__dict__.items():
        if k.startswith('_') or callable(v):
            continue
        try:
            field = instance._meta.get_field(k)
            if isinstance(field, BinaryField):
                v = force_text(base64.b64encode(v))
            elif isinstance(field, FileField):
                if not isinstance(v, six.string_types):
                    v = v.name
            # Check if the field is serializable. If not, we'll fall back
            # to serializing the DB values which should cover most use cases.
            try:
                json.dumps(v, cls=DjangoJSONEncoder)
            except TypeError:
                v = field.get_prep_value(v)
                k = SERIALIZED_DB_FIELD_PREFIX + k
        except FieldDoesNotExist:
            pass
        data[k] = v
    return json.loads(json.dumps(data, cls=DjangoJSONEncoder))





class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    """Custom SocialAccountAdapter for django-allauth.
    Replaced standard behavior for serialization of TimeZoneField.

    Need set it in project settings:
    SOCIALACCOUNT_ADAPTER = 'myapp.adapter.MySocialAccountAdapter'
    """

    def __init__(self, request=None):
        super(MySocialAccountAdapter, self).__init__(request=request)

    def pre_social_login(self, request, sociallogin):
        # This isn't tested, but should work
        try:
            emails = [email.email for email in sociallogin.email_addresses]
            user = CustomUserModel.objects.get(email__in=emails)
            sociallogin.connect(request, user)
            raise ImmediateHttpResponse(response=HttpResponse())
        except CustomUserModel.DoesNotExist:
            user=sociallogin.user
            user.username=user.email
            user.is_patient=1
            user.is_doctor=0
            user.save()
            sociallogin.connect(request, user)
            return redirect("index")
        except Exception as ex:
            logger.error(ex)

    def serialize_instance(self, instance):
        return my_serialize_instance(instance)

 