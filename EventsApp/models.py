# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from bootstrap_datepicker.widgets import DatePicker
from django import forms
from django.forms import ModelForm

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=150, blank=False, null=False)
    def __str__(self):
        return self.name

class EventType(models.Model):
    name = models.CharField(max_length=150, blank=False, null=False)
    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=150, blank=False, null=False)
    category = models.ForeignKey(Category)
    place = models.CharField(max_length=150, blank=False, null=False)
    initialDate = models.DateField(blank=False, null=False)
    finalDate = models.DateField(blank=False, null=False)
    eventType = models.ForeignKey(EventType)
    user = models.ForeignKey(User, null = False)

class Usuario(models.Model):
    auth_user_id = models.ForeignKey(User, null = False)

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['name','category','place','initialDate', 'finalDate', 'eventType' ]
        initialDate = forms.DateField(
          widget=DatePicker(options={"format": "mm/dd/yyyy","autoclose": True}))

class UserForm (ModelForm):
    class Meta :
        model = Usuario
        fields = ['id']

    nombre = forms.CharField(max_length=20)
    apellido = forms.CharField(max_length=20)
    email = forms.EmailField()
    nombre_usuario = forms.CharField(max_length=50)
    clave = forms.CharField(widget=forms.PasswordInput())
    confirme_clave = forms.CharField(widget=forms.PasswordInput())

    def clean_username(self):
        username = self.cleaned_data['nombre_usuario']
        if User.objects.filter(username=username):
            raise forms.ValidationError('Nombre de usuario ya registrado')
        return username

    def clean_password2(self):
        password = self.cleaned_data['clave']
        password2 = self.cleaned_data['confirme_clave']

        if password != password2:
            raise forms.ValidationError('Las claves no coinciden')
        return password2