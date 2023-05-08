from django.shortcuts import render

# Create your views here.

from .models import *

def index(request):
    """El home para App Odonto"""
    return render(request, 'Cargas/index.html')

def secciones(request):
    """"Secciones"""
    return render(request, 'Cargas/secciones.html')

def pacientes(request):
    """Muestra la sección Pacientes"""
    pacientes= Pacientes.objects.all()
    context= {'pacientes':pacientes}
    return render(request, 'Cargas/pacientes.html', context)

def presupuestos(request):
    """Muestra la sección Presupuestos"""
    presupuestos= Presupuestos.objects.all()
    context= {'presupuestos':presupuestos}
    return render(request, 'Cargas/presupuestos.html', context)

def cobranzas(request):
    """Muestra la sección Cobranzas"""
    cobranzas= Cobranzas.objects.all()
    presupuestos=Presupuestos.objects.all()
    context= {'cobranzas':cobranzas,'presupuestos':presupuestos}
    return render(request, 'Cargas/cobranzas.html', context)