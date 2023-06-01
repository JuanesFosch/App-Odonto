from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.db.models import Sum

# Create your views here.




from .models import *
from .forms import PacientesForm, PresupuestosForm, CobranzasForm

def index(request):
    """El home para App Odonto"""
    return render(request, 'Cargas/index.html',)

@login_required
def secciones(request):
    """"Secciones"""
    return render(request, 'Cargas/secciones.html')

@login_required
def carga_pacientes(request):
    """Permite a un usuario cargar pacientes"""
    if request.method != 'POST':
        # Sin datos cargados; crear una planilla en blanco.
        form= PacientesForm()
    else:
        # Datos cargados a través de POST, procesarlos.
        form= PacientesForm(data=request.POST)
        if form.is_valid():
            nuevo_paciente= form.save(commit=False)
            nuevo_paciente.owner = request.user
            form.save()
            return redirect('Cargas:carga_pacientes')
    # Muestra una planilla en blanco o inválida.
    context= {'form': form}
    return render(request,'Cargas/carga_pacientes.html', context )

@login_required
def pacientes(request):
    """Muestra la sección Pacientes"""
    pacientes= Pacientes.objects.filter(owner=request.user)
    context= {'pacientes':pacientes}
    return render(request, 'Cargas/pacientes.html', context)

@login_required
def editar_pacientes(request, dni):
    """Permite editar los datos de un paciente""" 
    paciente_dni= Pacientes.objects.get(DNI=dni)
    nombre= paciente_dni.Nombre
    
    if request.method != 'POST':
        # Initial request; pre-fill form with the current entry.
        form = PacientesForm(instance=paciente_dni)
    else:
        # POST data submitted; process data.
        form = PacientesForm(instance=paciente_dni,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('Cargas:pacientes')
    
    context = {'paciente_dni': paciente_dni, 'nombre': nombre, 'form': form}
    return render(request, 'Cargas/editar_pacientes.html', context)
    

@login_required
def carga_presupuestos(request):
    """Permite a un usuario cargar presupuestos"""
    if request.method != 'POST':
        # Sin datos cargados; crear una planilla en blanco.
        form= PresupuestosForm(owner=request.user)
    else:
        # Datos cargados a través de POST, procesarlos.
        form= PresupuestosForm(data=request.POST,owner=request.user)
        if form.is_valid():
            nuevo_presupuesto= form.save(commit=False)
            nuevo_presupuesto.owner = request.user
            form.save()
            return redirect('Cargas:carga_presupuestos')
    # Muestra una planilla en blanco o inválida.
    context= {'form': form}
    return render(request,'Cargas/carga_presupuestos.html', context )

@login_required
def carga_cobranzas(request):
    """Permite a un usuario cargar cobranzas"""
    if request.method != 'POST':
        # Sin datos cargados; crear una planilla en blanco.
        form= CobranzasForm(owner=request.user)
    else:
        # Datos cargados a través de POST, procesarlos.
        form= CobranzasForm(data=request.POST,owner=request.user)
        if form.is_valid():
            nueva_cobranza= form.save(commit=False)
            nueva_cobranza.owner = request.user
            form.save()
            return redirect('Cargas:carga_cobranzas')
        else:
            form = CobranzasForm(owner=request.user)
    # Muestra una planilla en blanco o inválida.
    context= {'form': form}
    return render(request,'Cargas/carga_cobranzas.html', context )


@login_required
def presupuestos_y_cobranzas(request):
    """Muestra las secciones Presupuestos y Cobranzas"""
    
    presupuestos_p= Presupuestos.objects.filter(owner=request.user)
    context_presupuestos= []
    context={}  # Para evitar errores en el caso de que el usuario no tenga Presupuestos o Cobranzas cargadas,
                # se crea vacío el diccionario 'context' necesario para la función 'render' del final. 
    cobranzas= Cobranzas.objects.filter(owner=request.user)  # Se obtiene un queryset los campos de la tabla Cobranzas.
    context_cobranzas = []   # Es una lista que se va a llenar con diccionarios
    for cobranza in cobranzas:
        # Se obtiene el número de comprobante de cada cobranza.
        número_de_comprobante=cobranza.Número_de_comprobante
        # Se obtiene un queryset con el número de orden de cada Cobranza. Es decir a qué Presupuesto existente corresponde cada cobro.
        presupuestos_c=Presupuestos.objects.filter(Cobranzas__Número_de_comprobante=f"{número_de_comprobante}").distinct()
        # Se obtiene el valor del número de orden dentro del queryset.
        valores=presupuestos_c.values_list('Número_de_orden', flat=True)
        # Se llena la lista creada antes del bucle For con los resultados de las consultas.
        context_cobranzas.append({
            'cobranza': cobranza,
            'presupuestos': valores
        })           # Se usa la lista llenada como contexto para pasar a la función 'render'
        context = {'context_cobranzas': context_cobranzas}
        
    #--Lo siguiente calcula el Saldo, trae los números de comprobantes de cada pago y termina de armar el contexto para pasar a la función 'render' 
    for presupuesto in presupuestos_p:
        orden=presupuesto.Número_de_orden
        monto=presupuesto.Monto
        cuánto_pagó=Cobranzas.objects.filter(Número_de_orden=orden).values_list('Cuánto_pagó', flat=True).aggregate(Sum("Cuánto_pagó"))
        números_de_comprobante=Cobranzas.objects.filter(Número_de_orden=orden).values_list('Número_de_comprobante', flat=True) 
        saldo= monto - cuánto_pagó['Cuánto_pagó__sum'] if cuánto_pagó['Cuánto_pagó__sum'] else monto
        context_presupuestos.append({
                        'presupuesto': presupuesto,
                        'saldo': saldo,
                        'números_de_comprobante':números_de_comprobante
            })     
    context['context_presupuestos'] = context_presupuestos
    return render(request, 'Cargas/presupuestos_y_cobranzas.html', context)
        

@login_required
def editar_presupuestos(request, orden):
    """Permite editar los datos de un presupuesto""" 
    número= Presupuestos.objects.get(Número_de_orden=orden)
    owner_id= número.owner_id
    
    if request.method != 'POST':
        # Initial request; pre-fill form with the current entry.
        form = PresupuestosForm(instance=número, owner=owner_id)
    else:
        # POST data submitted; process data.
        form = PresupuestosForm(instance=número,owner=owner_id,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('Cargas:presupuestos_y_cobranzas')
    
    context = {'número': número, 'form': form}
    return render(request, 'Cargas/editar_presupuestos.html', context)


@login_required
def editar_cobranzas(request, comprobante):
    """Permite editar los datos de una cobranza""" 
    número= Cobranzas.objects.get(Número_de_comprobante=comprobante)
    owner_id= número.owner_id
   
    if request.method != 'POST':
        # Initial request; pre-fill form with the current entry.
        form = CobranzasForm(instance=número, owner=owner_id)
    else:
        # POST data submitted; process data.
        form = CobranzasForm(instance=número,owner=owner_id,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('Cargas:presupuestos_y_cobranzas')
    
    context = {'número': número, 'form': form}
    return render(request, 'Cargas/editar_cobranzas.html', context)




