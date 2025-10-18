from django.db import models

# Create your models here.

from django import forms
class CredencialForm(forms.Form):
    foto = forms.ImageField(required=False, label="Foto")  # Campo para subir imagen
    nombre_completo = forms.CharField(max_length=100, label="Nombre Completo")
    cargo = forms.CharField(max_length=100, label="Cargo")
    pais = forms.CharField(max_length=100, label="País")