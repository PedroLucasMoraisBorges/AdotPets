from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Room, Message
from pages.utilits import getDefaultUser
from django.db.models import Q
from datetime import date, datetime
from auth_user.models import ProfileImage
from django.contrib import messages

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

    receiverImg = ProfileImage.objects.filter(fk_user=currentChatUser).first()

    context = {"room_details":room_details, 'username':username, 'currentChatUser':currentChatUser, 'room_id':room_id, "info":getDefaultUser(request.user), "receiverImg":receiverImg, 'nChat' : 'nChat'}
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

def chatsPage(request):
    hasChats = False
    rooms = []
    active_chats = Room.objects.filter(Q(fk_donor=request.user) | Q(fk_donee=request.user))

    if active_chats.count() > 0:
        hasChats = True
        for chat in active_chats:
            receiver = None

            if request.user == chat.fk_donor:
                receiver = chat.fk_donee
            elif request.user == chat.fk_donee:
                receiver = chat.fk_donor

            unreadMessages = Message.objects.filter(fk_room=chat, status="UNREAD").exclude(fk_sender=request.user).count()
            
            lastMessage = Message.objects.filter(fk_room = chat).order_by('created').last()
            if lastMessage != None:
                messageDate = lastMessage.created.date()
                todayDate = date.today()
                if messageDate == todayDate:
                    lastMessageDate = lastMessage.created.time()
                else:
                    dias = (todayDate - messageDate).days
                    if dias == 1:
                        lastMessageDate = "Ontem"
                    elif dias > 1:
                        lastMessageDate = str(dias) + " dias atrás"
            else:
                lastMessageDate = None

            roomDate = chat.created.date()


            rooms.append(
                {
                    'details': chat,
                    'receiver': receiver,
                    'lastMessage': lastMessage,
                    'lastMessageDate': lastMessageDate,
                    'roomDate': roomDate,
                    'unreadMessages': unreadMessages,
                    'receiverImg': ProfileImage.objects.filter(fk_user=receiver).first(),
                }
            )

    
    if request.method == "POST" and "deleteChatButton" in request.POST:
        roomId = request.POST.get("chatId")
        try:
            room = Room.objects.get(id=roomId)
            room.delete()
            mensagem = "Chat deletado com sucesso!"
            messages.success(request, mensagem)
            return redirect('chatsPage')
        except:
            return HttpResponse("Fatal Error, Chat a ser deletado não existe!")


    context = {"info":getDefaultUser(request.user), 'hasChats':hasChats, 'rooms':rooms, 'nChat' : 'nChat'}
    
    return render(request, "chat/chats.html", context);
