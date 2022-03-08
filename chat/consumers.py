# chat/consumers.py
from asyncio.windows_events import NULL
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from chat.views import updateOffline
from onlinedoctor.models import CustomUserModel, appointmentModel
import datetime
from chat.models import Message, Room
from channels.db import database_sync_to_async
from django.utils.timezone import localtime



class ChatConsumer(WebsocketConsumer):

    starting_conferance_time=datetime.datetime.min
    finishing_conferance_time=datetime.datetime.min
    difference=datetime.datetime.min
    

    def close_Socket(self,data):
        user=get_object_or_404(CustomUserModel,username=data["requested"])
        if user.is_active_now == False:
            user.online="onsite"
        else:
            user.online="offline"
        user.save()
       

    @database_sync_to_async
    def adding(self,data):
       # user=get_object_or_404(CustomUserModel,username=data["requestUser"])
        user=get_object_or_404(CustomUserModel,username=data["requestUser"])
        user.online="online"
        user.save()
        content={
            "command":"online",
            "class":"avatar avatar-online",
            "action":user.username,
        }
        self.send_message(content)
    

    @database_sync_to_async
    def decreasing(self,data):
        user=get_object_or_404(CustomUserModel,username=data["requestUser"])
        user.online="offline"
        user.save()
        content={
            "command":"offline",
            "class":"avatar avatar-offline",
            "action":user.username,
        }
        self.send_message(content)


    def fetch_messages(self,data):   
        messages=Message.objects.filter(room=data["roomName"]).all()
        name = data["name"]
        # we will use this as room name as well
        self.my_name = name
        # Join room
        async_to_sync(self.channel_layer.group_add)(
            self.my_name,
            self.channel_name
        )
        content={
            "command":"messages",
            "messages":self.messages_to_json(messages),
        }
        self.send_message(content)

    def new_message(self,data): 
        what_is_it=data["what_is_it"]
        fileName=data["fileName"]
        second_user_username=data["to"]
        second_user=get_object_or_404(CustomUserModel,username=second_user_username)   
        first_user_username=data["first_user"]
        room=get_object_or_404(Room,id=data["roomName"])
        first_user=get_object_or_404(CustomUserModel,username=first_user_username)    
        message=Message.objects.create(first_user=first_user,second_user=second_user,content=data["message"],room=room,what_is_it=what_is_it,fileName=fileName)
     #   print(message.room+" mesaj room")
        content={
            "command":"new_message",
            "message":self.message_to_json(message),
        }
        return self.send_chat_message(content)


    def messages_to_json(self,messages):
        result=[]
        for message in messages:
            result.append(self.message_to_json(message))
        return result


    #str(message.created_date).split(":")[0]+":"+str(message.created_date).split(":")[1],

    def message_to_json(self,message):
        okey="true"
        appos=appointmentModel.objects.filter(id=message.room.appointment.id)
        if appos.count()>0:
            messageSendTime=localtime(message.created_date).time().strftime("%H:%M")
            finish_time = datetime.datetime.strptime(appos[0].finishing_time, '%H:%M')
            finish_time=finish_time.time().strftime("%H:%M")
            if messageSendTime>finish_time:
                okey="false"

        return{
            "first_user":message.first_user.username,
            "second_user":message.second_user.username,
            "room":str(message.room.id),
            "content":message.content,
            "created_date":str(localtime(message.created_date).hour)+":"+str(localtime(message.created_date).minute),
            "is_read":message.is_read,
            "what_is_it":message.what_is_it,
            "fileName":message.fileName,
            "image":message.first_user.image.url,
            "is_okey":okey
        }

    
        
    
    def typing(self, event):
        self.send(text_data=json.dumps({
            'command': 'typing',
            'data': event['data']
        }))

    
    def defineType(self, event):
        self.send(text_data=json.dumps({
            'command': 'callType',
            'data': event['data']
        }))

   

    commands={
        "fetch_messages":fetch_messages,
        "new_message":new_message,
        "closeSocket":close_Socket,
    }

    
    # @database_sync_to_async
    # def update_user_incr(self, user):
    #     CustomUserModel.objects.filter(pk=request.user.pk).update(online=F('online') + 1)


 



    def call(self,data): 
        self.starting_conferance_time=datetime.datetime.now()
        self.name = data['data']['name']
        print(self.my_name, "is calling", self.name)
        print("call fonksiyonunda consumer.py")
        
        async_to_sync(self.channel_layer.group_send)(
            self.name,
            {
                'type': 'call_received',
                'command': 'call_received',
                'data': {
                    'caller': self.my_name,
                    'otherUserFullName':data['data']['otherUserFullName'],
                    'rtcMessage': data['data']['rtcMessage']
                }
            }
        )
    
    def answer_call(self,data): 
        print("answer_call fonksiyonunda consumer.py")
        self.caller = data['data']['caller']
        print(self.my_name, "is answering", self.caller, "calls.")

        async_to_sync(self.channel_layer.group_send)(
            self.caller,
            {
                'type': 'call_answered',
                'command': 'call_answered',
                'data': {
                    'rtcMessage': data['data']['rtcMessage'],
                    'otherUserFullName':data['data']['otherUserFullName']
                }
            }
        )
       

   
    def rejectCall(self, event):
        self.send(text_data=json.dumps({
            'command': 'rejectCall',
            'data': event['data']
        }))
      
    def call_received(self, event):
        print("call_received fonksiyonunda consumer.py")
        print('Call received by ', self.my_name )
        self.send(text_data=json.dumps({
            'command': 'call_received',
            'data': event['data']
        }))


    def call_answered(self, event):
        print("call_answered fonksiyonunda consumer.py")
        print(self.my_name, "'s call answered")
        self.send(text_data=json.dumps({
            'command': 'call_answered',
            'data': event['data']
        }))

    
    def ICEcandidate(self, event):
        self.send(text_data=json.dumps({
            'command': 'ICEcandidate',                 #burayı kontrol et s li değilde normal yazılabilir
            'data': event['data']
        }))

    


    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        print("web socket chat connected ")
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        print("web socket chat closed")
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
       
     
        

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        print("receive kısmı")
        if(data["command"]=="call"):
            print("evet call kısmında")
            self.call(data)
        elif(data["command"]=="defineStartTime"):
            self.starting_conferance_time=datetime.datetime.now()
        elif(data["command"]=="answer_call"):
            self.starting_conferance_time=datetime.datetime.now()
            print("evet answer_call kısmında")
            self.answer_call(data)
        elif(data["command"]=="rejectCall"):
            self.finishing_conferance_time=datetime.datetime.now()
            print("rejectCall ......")
            self.difference=self.finishing_conferance_time-self.starting_conferance_time
            rooma=Room.objects.get(id=self.room_name)
            print("difference time")
            print(self.difference)
            if rooma.totalDurationTime==None or rooma.totalDurationTime==NULL:
                rooma.totalDurationTime=datetime.datetime.min.time()
                rooma.save()
            rooma.totalDurationTime=(datetime.datetime.combine(datetime.date(1,1,1),rooma.totalDurationTime) + self.difference).time()
            rooma.save()
            rooma.appointment.totalDuration=rooma.totalDurationTime
            rooma.appointment.save()

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'rejectCall',
                    'command': 'rejectCall',
                    'data':{}
                }
            )
        elif(data["command"]=="ICEcandidate"):
            self.user = data['data']['user']
            print("evet ICEcandidate kısmında")
            async_to_sync(self.channel_layer.group_send)(
                self.user,
                {
                    'type': 'ICEcandidate',
                    'command': 'ICEcandidate',
                    'data': {
                        'rtcMessage': data['data']['rtcMessage'],
                        'otherUserFullName':data['data']['otherUserFullName'],
                    }
                }
            )
        elif(data["command"]=="typing"):
            userSlug=data["otherUser"]
            user=CustomUserModel.objects.get(slug=data["requested"])
            async_to_sync(self.channel_layer.group_send)(
                userSlug,
                {
                    'type': 'typing',
                    'command': 'typing',
                    'data': {
                        "image":user.image.url
                    }
                }
            )
        elif(data["command"]=="defineType"):
            print(data["callType"])
            print("gelen call type")
            userSlug=data["otherUser"]
            print(userSlug)
            async_to_sync(self.channel_layer.group_send)(
                userSlug,
                {
                    'type': 'defineType',
                    'command': 'defineType',
                    'data': {
                        "callType":data["callType"]
                    }
                }
            )
           
        else:
            self.commands[data["command"]](self,data)



    def send_chat_message(self,message):    
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
              
            }
        )



    def send_message(self,message):
        self.send(text_data=json.dumps(message))


    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        # Send message to WebSocket
        self.send(text_data=json.dumps(message))




