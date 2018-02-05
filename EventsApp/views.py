# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from models import *
from django.shortcuts import render
import json
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout

from django.http import JsonResponse

from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.views.decorators.csrf import csrf_exempt
from django import forms

from serializers import *
from rest_framework import generics, viewsets
from rest_framework import permissions
from rest_framework import mixins
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
# Create your views here.

def index(request):
    context = { }
    if request.user.is_authenticated():
        list = Event.objects.filter(user=request.user.id)
        print list
        print request.user.id
        context = {'Events': list}
    return render(request, 'index.html', context)

def registro (request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            data = form.cleaned_data
            username = data.get('nombre_usuario')
            first_name = data.get('nombre')
            last_name = data.get('apellido')
            password = data.get('clave')
            email = data.get('email')

            user_model = User.objects.create_user(username=username, password=password)
            user_model.first_name = first_name
            user_model.last_name = last_name
            user_model.email = email

            user_app = Usuario(auth_user_id = user_model);
            user_model.save()
            user_app.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        form = UserForm()
        context = {'form' : form}
    return render(request, 'register.html', context)

def createEvent (request):
    form = EventForm()
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            print  'entro'
            data = form.cleaned_data
            print data
            name = data.get('name')
            category = data.get('category')
            place = data.get('place')
            initialDate = data.get('initialDate')
            finalDate = data.get('finalDate')
            eventType = data.get('eventType')
            user = request.user.id
            print category
            user_app = Usuario(name= name, category=category,place=place,initialDate=initialDate,finalDate=finalDate,eventType=eventType,user=user);
            user_app.save()
            return HttpResponseRedirect(reverse('index'))

    form = EventForm()
    context = {'form' : form}
    return render(request, 'createEvent.html', context)

def login_view(request):
    if request.user.is_authenticated():
        return redirect(reverse('index'))
    mensaje = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('index'))
        else:
            mensaje = 'Nombre de usuario o clave invalido'

    return render(request,'login.html',{'mensaje':mensaje})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@csrf_exempt
def getCategories(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        print categories
        return JsonResponse({'message': 'Done','data':categories})

class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Products to be viewed or edited.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class EventTypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Products to be viewed or edited.
    """
    queryset = EventType.objects.all()
    serializer_class = EventTypeSerializer

class EventViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Products to be viewed or edited.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer

