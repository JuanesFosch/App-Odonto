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
    cobranzas= Cobranzas.objects.all()  # Se obtiene un queryset los campos de la tabla Cobranzas.
    context_list = []
    for cobranza in cobranzas:
        # Se obtiene el número de comprobante de cada cobranza.
        número_de_comprobante=cobranza.Número_de_comprobante
        # Se obtiene un queryset con el número de orden de cada Cobranza. Es decir a qué Presupuesto existente corresponde cada cobro.
        presupuestos=Presupuestos.objects.filter(Cobranzas__Número_de_comprobante=f"{número_de_comprobante}").distinct()
        # Se obtiene el valor del número de orden dentro del queryset.
        valores=presupuestos.values_list('Número_de_orden', flat=True)
        # Se llena la lista creada antes del bucle For con los resultados de las consultas.
        context_list.append({
            'cobranza': cobranza,
            'presupuestos': valores
        })
        # Se usa la lista llena como contexto para pasar a la función 'render'
        context = {'context_list': context_list}
    return render(request, 'Cargas/cobranzas.html', context)

