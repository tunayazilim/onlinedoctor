import datetime
import django
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models.fields import EmailField
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from chat.models import Message, Room, peerInformations
from django.utils import timezone
from onlinedoctor.models import CustomUserModel, appointmentModel
from onlinedoctor.views import deletedAppoitments




#randevular onaylandığında iki kullanıcı arasında room oluşturmak
#her usera tıklandığında room name value değişecek

@login_required(login_url="login")
def indexChat(request):
    other_user=""
    deletedAppoints=list()
    appointments=list()
    rooms=list()
    if request.user.is_patient:
        appoints=appointmentModel.objects.filter(patient=request.user,date__lte=datetime.datetime.today())
        if appoints.count()>0:
            for i in appoints:
                if i.date==datetime.datetime.today().date():
                    starting_time = datetime.datetime.strptime(i.starting_time, '%H:%M')
                    starting_time=starting_time-datetime.timedelta(minutes=6)
                    starting_time=starting_time.time().strftime("%H:%M")
                    finishing_time = datetime.datetime.strptime(i.finishing_time, '%H:%M')
                    finishing_time=finishing_time.time().strftime("%H:%M")
                    now_time=datetime.datetime.now().time().strftime("%H:%M")
                    if now_time > starting_time and now_time < finishing_time:
                        appointments.append(i)
                    if now_time > finishing_time:  
                        deletedAppoints.append(i)
                else:
                    deletedAppoints.append(i)

        for i in appointments:
            room=Room.objects.get(appointment=i)
            rooms.append(room)
        type="patient"
        if rooms:
            other_user=rooms[0].first_user
    elif request.user.is_doctor:
        appoints=appointmentModel.objects.filter(doctor=request.user,date__lte=datetime.datetime.today())
        if appoints.count()>0:
            for i in appoints:
                if i.date==datetime.datetime.today().date():
                    starting_time = datetime.datetime.strptime(i.starting_time, '%H:%M')
                    starting_time=starting_time-datetime.timedelta(minutes=6)
                    starting_time=starting_time.time().strftime("%H:%M")
                    finishing_time = datetime.datetime.strptime(i.finishing_time, '%H:%M')
                    finishing_time=finishing_time.time().strftime("%H:%M")
                    now_time=datetime.datetime.now().time().strftime("%H:%M")
                    if now_time > starting_time and now_time < finishing_time:
                        appointments.append(i)
                    if now_time > finishing_time:
                        deletedAppoints.append(i)
                else:
                    deletedAppoints.append(i)
        for i in appointments:
            room=Room.objects.get(appointment=i)
            rooms.append(room)
        type="doctor"
        if rooms:
            other_user=rooms[0].second_user
    for i in deletedAppoints:       
        room=Room.objects.filter(appointment=i)
        if room.count()>0:
            room[0].delete()
    deletedAppoints.clear()     

    if other_user != "":
        return render(request, 'chat/index.html',{
            "chatMessageFooter":"a",
            "rooms":rooms,
            'room_name': rooms[0].id,
            # "room":room,
            "other_user":other_user,
            "typeOfUser":type,
            "whichPage":"chatPage",

        })
    else:
        return render(request, 'chat/noChat.html',{

        })



def room(request, room_name):
    users=CustomUserModel.objects.filter(is_active=True).exclude(email=request.user.email)
    room=Room.objects.get(id=room_name)
    return render(request, 'chat/room_v2.html', {
        'room_name': room_name,
        "chatMessageFooter":"a",
        "room":room,
        "users":users,
    })




def startChat(request,slug):
    second_user=get_object_or_404(CustomUserModel,slug=slug)
    try:
        room=Room.objects.get(first_user=request.user,second_user=second_user)
    except Room.DoesNotExist:
        try:
            room=Room.objects.get(second_user=request.user,first_user=second_user)
        except Room.DoesNotExist:
            room=Room.objects.create(first_user=request.user,second_user=second_user)
    return redirect("room",room.id)




def createMessage(request,slug,room,message):
    second=CustomUserModel.objects.get(slug=slug)
    Message.objects.create(first_user=request.user,second_user=second,room=room,content=message)




def get_user(request,room_id):
    # print(request.GET)
    # print("get user")
    if request.method=='GET' and request.is_ajax():
        second_user=""
        otherUserPeerId=""
        otherUserFullName=""
        if request.user.online != "online":
            request.user.online="online"
            request.user.save()
        room=get_object_or_404(Room,id=room_id)
        appo=appointmentModel.objects.get(id=room.appointment.id)
        start_time = datetime.datetime.strptime(appo.starting_time, '%H:%M')
        start_time=start_time.time()
        now_time=datetime.datetime.now().time()
        if now_time>=start_time:
            show=datetime.datetime.combine(datetime.date.today(), now_time) - datetime.datetime.combine(datetime.date.today(), start_time)
            show=show.seconds
        else:
            show=0

        if request.user.is_doctor:
            user=room.second_user
            otherUserFullName=user.get_full_name()
            peerUser=get_object_or_404(peerInformations,user=user)
            if peerUser:
                pass
            else:
                peerUser=peerInformations.objects.create(user=user)
            otherUserPeerId=peerUser.peerId
            second_user=room.second_user.get_doctor_name()
        elif request.user.is_patient:
            user=room.first_user
            otherUserFullName=user.get_doctor_name()
            peerUser=get_object_or_404(peerInformations,user=user)
            if peerUser:
                pass
            else:
                peerUser=peerInformations.objects.create(user=user)
            otherUserPeerId=peerUser.peerId
            second_user=room.first_user.get_full_name()

        if user.online == "online":
            className= "avatar avatar-online"
        elif user.online == "offline":
            className= "avatar avatar-offline"
        elif user.online == "onsite":
            className= "avatar avatar-away"
        data ={
                "second_user_name":second_user,
                "image":user.image.url,
                "slug":user.slug,
                "otherUserPeerId":otherUserPeerId,
                # "messages":list(Message.objects.filter(room_id=room_id).all().values()),
                "className":className,
                "otherUserFullName":otherUserFullName,
                "imageUrl":user.image.url,
                "appointmentDuration":appo.duration,
                "appointmentStartTime":show,
        }
        return JsonResponse(data,safe=True)
    return JsonResponse({'status':'Fail', 'msg': 'Object does not exist'})






def updateOffline(usernmae):
    user=get_object_or_404(CustomUserModel,email=usernmae)
    user.online="onsite"
    user.save()




@login_required(login_url="login")
def videoCall(request):
   # other_user=get_object_or_404(CustomUserModel,slug=slug)
    #print(other_user.username+ " fonk calısıyor ve kullanicimiz")
    # if other_user.is_doctor:
    #     room=get_object_or_404(Room,first_user=other_user,second_user=request.user)
    #     full_name=other_user.get_doctor_name()
    # elif other_user.is_patient:
    #     room=get_object_or_404(Room,first_user=request.user,second_user=other_user)
    #     full_name=other_user.get_full_name()

    context={
      #  "other_user":other_user,
        "room":room,
        # "chatMessageFooter":"ers",
      #  "full_name":full_name,
        "videoCall":"sodf",
        "whichPage":"videoPage",
    }
    return render(request,"chat/video-call.html",context)
