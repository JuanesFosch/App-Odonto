from django.shortcuts import render, redirect

# Create your views here.

from .models import *
from .forms import PacientesForm, PresupuestosForm, CobranzasForm

def index(request):
    """El home para App Odonto"""
    return render(request, 'Cargas/index.html')

def secciones(request):
    """"Secciones"""
    return render(request, 'Cargas/secciones.html')

def carga_pacientes(request):
    """Permite a un usuario cargar pacientes"""
    if request.method != 'POST':
        # Sin datos cargados; crear una planilla en blanco.
        form= PacientesForm()
    else:
        # Datos cargados a través de POST, procesarlos.
        form= PacientesForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('Cargas:carga_pacientes')
    # Muestra una planilla en blanco o inválida.
    context= {'form': form}
    return render(request,'Cargas/carga_pacientes.html', context )


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

def carga_presupuestos(request):
    """Permite a un usuario cargar presupuestos"""
    if request.method != 'POST':
        # Sin datos cargados; crear una planilla en blanco.
        form= PresupuestosForm()
    else:
        # Datos cargados a través de POST, procesarlos.
        form= PresupuestosForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('Cargas:carga_presupuestos')
    # Muestra una planilla en blanco o inválida.
    context= {'form': form}
    return render(request,'Cargas/carga_presupuestos.html', context )

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

def carga_cobranzas(request):
    """Permite a un usuario cargar cobranzas"""
    if request.method != 'POST':
        # Sin datos cargados; crear una planilla en blanco.
        form= CobranzasForm()
    else:
        # Datos cargados a través de POST, procesarlos.
        form= CobranzasForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('Cargas:carga_cobranzas')
    # Muestra una planilla en blanco o inválida.
    context= {'form': form}
    return render(request,'Cargas/carga_cobranzas.html', context )