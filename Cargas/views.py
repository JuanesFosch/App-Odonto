from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.db.models import Sum

# Create your views here.

#----Pruebas de otros proyectos---

from django.http import HttpResponse 
try:     
    # Python2
    from urllib2 import urlopen
except ImportError:
    # Python3
    from urllib.request import urlopen

import PIL.Image
import io
import requests
import base64
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
#--------------------------------


from .models import *
from .forms import PacientesForm, PresupuestosForm, CobranzasForm

def index(request):
    """El home para App Odonto"""
    return render(request, 'Cargas/index.html',)

def prueba_imagen(request):
    """Prueba para usar en la aplicación DACC"""
    total_url = "https://www2.contingencias.mendoza.gov.ar/radar/latest.gif" 
    r = requests.get(total_url)
    imagen_base64 = base64.b64encode(r.content).decode('utf-8')
    return render(request,'Cargas/imagen.html',{'imagen_base64': imagen_base64})


def prueba_grafico(request):
    """Prueba para usar en la aplicación BCRA"""
    datos= r"C:\Users\juanf\Desktop\App BCRA\datos_completo.csv"
    df=pd.read_csv(datos)
    df["Fecha"] = pd.to_datetime(df.Fecha,format='mixed')
    df["Badlar"]=df["Badlar"].str.strip()
    df["Badlar"] = pd.to_numeric(df["Badlar"].replace(",", ".", regex=True))
    df["CER"]=df["CER"].str.strip()
    df["CER"] = pd.to_numeric(df["CER"].replace(",", ".", regex=True))
    df["UVA"]=df["UVA"].str.strip()
    df["UVA"] = pd.to_numeric(df["UVA"].replace(",", ".", regex=True))
    plt.style.use('ggplot')
    df.plot("Fecha", ["Badlar","CER","UVA"],
            kind="line",
            figsize=(10,6),
            color=["GREEN","darkblue","RED"],
            title="ANÁLISIS DE TASAS",
            ylabel = "Tasa",
            xlabel = "Fecha",
            mouseover=True)
    grafico=plt.show()
    return render(request,'Cargas/imagen.html',{'grafico': grafico})

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