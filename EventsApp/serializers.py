from django.contrib.auth.models import User, Group
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework import viewsets
from .models import *

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')

class EventTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EventType
        fields = ('id', 'name')

class EventSerializer(serializers.HyperlinkedModelSerializer):
    category = CategorySerializer(many=False, read_only=True)
    eventType = EventTypeSerializer(many=False, read_only=True)
    class Meta:
        model = Event
        fields = ('id','name','category','place','initialDate', 'finalDate', 'eventType' )