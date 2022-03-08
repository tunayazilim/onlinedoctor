from django.urls import path
from .views import(
    indexChat,room,startChat,createMessage,get_user,updateOffline,videoCall
)




urlpatterns = [
    path('', indexChat, name='indexChat'),
    path('<str:room_name>/', room, name='room'),
    path('startChat/<slug:slug>/', startChat, name='startChat'),
    path('createMessage/<slug:slug>/<str:room>/<str:message>/', createMessage, name='createMessage'),
    path('get_user/<str:room_id>', get_user, name='get_user'),
    # path('updateOffline', updateOffline, name='updateOffline'),
    path('videoCall', videoCall, name='videoCall'),
]