from multiprocessing import context
from onlinedoctor.models import CustomUserModel, appointmentModel, deletedAppointmentModel
from django import template



register=template.Library()


@register.simple_tag
def notificationsOfAdmin():
    notifications=list()
    for i in CustomUserModel.objects.filter(is_doctor=True,doctor_okey=False):
        context={
            "type":"waitingDoctor",
            "user":i
        }
        notifications.append(context)
    
    for i in appointmentModel.objects.all():
        context={
            "type":"appointment",
            "appointment":i
        }
        notifications.append(context)
    
    for i in deletedAppointmentModel.objects.all():
        context={
            "type":"deletedAppointment",
            "appointment":i
        }
        notifications.append(context)

    return notifications


