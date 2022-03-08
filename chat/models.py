from django.db import models
import uuid
from onlinedoctor.models import CustomUserModel, appointmentModel
from io import BytesIO
import sys
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile



class Room(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4)
    first_user=models.ForeignKey(CustomUserModel,related_name="room_first",on_delete=models.CASCADE,null=True)
    second_user=models.ForeignKey(CustomUserModel,related_name="room_second",on_delete=models.CASCADE,null=True)
    appointment=models.ForeignKey(appointmentModel,related_name="appoRoom",on_delete=models.CASCADE,null=True,blank=True)
    appoitmentDayandTime=models.DateTimeField(null=True,blank=True)
    totalDurationTime=models.TimeField(null=True,blank=True)

    def get_last_message_minute(self):
        obj=Message.objects.filter(room_id=self.id).last()
        if obj:
            return obj.created_date
        else:
            return None

    def get_last_message(self):
        obj=Message.objects.filter(room_id=self.id).last()
        if obj:
            return obj
        else:
            return None

       




class Message(models.Model):
    first_user=models.ForeignKey(CustomUserModel,related_name="messagesoffirst_user",verbose_name="Kullanıcı1",on_delete=models.CASCADE,null=True)
    second_user=models.ForeignKey(CustomUserModel,related_name="messagesof_second_user",verbose_name="Kullanıcı2",on_delete=models.CASCADE,null=True)
    room=models.ForeignKey(Room,related_name="messages",verbose_name="Oda",on_delete=models.CASCADE)
    content=models.TextField(verbose_name="Mesaj içeriği")
    created_date=models.DateTimeField(auto_now_add=True)
    is_read=models.BooleanField(default=False)
    what_is_it=models.CharField(max_length=50,null=True,default="text")
    fileName=models.CharField(max_length=50,null=True,default="")
    




class peerInformations(models.Model):
    user = models.ForeignKey(CustomUserModel,on_delete=models.CASCADE)
    peerId=models.CharField(max_length=150,blank=True,null=True,default="")  
    callType=models.CharField(max_length=50,null=True,default="")
    