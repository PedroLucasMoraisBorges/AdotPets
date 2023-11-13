from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Room, Message

# Create your views here.

def chatRoom(request, pk):
    try:
        room = Room.objects.get(id=pk)
    except:
        return HttpResponse("Este chat não existe!")
    
    if request.user != room.fk_donee and request.user != room.fk_donor:
        return HttpResponse("Você não tem acesso a esse chat!")

    username = request.user.username
    room_details = Message.objects.filter(fk_room=room)
    room_id = room.id

    if room.fk_donee == request.user:
        currentChatUser = room.fk_donor
    elif room.fk_donor == request.user:
        currentChatUser = room.fk_donee

    context = {"room_details":room_details, 'username':username, 'currentChatUser':currentChatUser, 'room_id':room_id}
    return render(request, "chat/room.html", context)

def Send(request):
    message = request.POST.get("message")
    room_id = request.POST.get("room_id")
    room = Room.objects.get(id=room_id)
    new_message = Message.objects.create(content=message, fk_sender=request.user, fk_room=room)
    new_message.save()
    return HttpResponse("Message saved sucessfuly!")
    
def getMessages(request, pk):
    room = Room.objects.get(id=pk)
    messages = Message.objects.filter(fk_room=room)
    return JsonResponse({"messages":list(messages.values())})

