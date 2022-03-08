import calendar
import datetime
from onlinedoctor.models import footerModel
from django import template

from onlinedoctor.views import getDayEnglish



register=template.Library()


@register.simple_tag
def dates(day):
    day=getDayEnglish(day)
    my_date = datetime.date.today()
    a = calendar.day_name[my_date.weekday()]  
    if(a!="Monday" and a!="Tuesday" and a!="Wednesday" and a!="Thursday" and a!="Friday" and a!="Saturday" and a!="Sunday"):
        a=getDayEnglish(a)
    weekdays = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    now = weekdays.index(a)
    coming_day_index = weekdays.index(day)
    if coming_day_index<now:
        date = my_date + datetime.timedelta(days= 7+coming_day_index-now)
    else:
        date=my_date + datetime.timedelta(days= coming_day_index-now)
    return date