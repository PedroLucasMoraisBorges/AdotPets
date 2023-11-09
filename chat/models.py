from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Room(models.Model):
    fk_donee = models.ForeignKey(User, related_name="roomParticipant", on_delete=models.CASCADE)
    fk_donor = models.ForeignKey(User, related_name="roomHost", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class Message(models.Model):
    fk_room = models.ForeignKey(Room, related_name="room", on_delete=models.CASCADE)
    fk_sender = models.ForeignKey(User, related_name="sender", on_delete=models.SET_NULL, null=True)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

