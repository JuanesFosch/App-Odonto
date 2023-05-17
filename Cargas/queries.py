from Cargas.models import Presupuestos, Cobranzas, Tratamientos_Propios,Tratamientos_ObrasSociales_Prepagas, Pacientes

Propios=Tratamientos_Propios.objects.all()
for valor in Propios:
    print(valor.Código_interno)  #---Esta es la posta
for valor in Propios:
    print(valor.Tratamiento)

valores=Propios.values_list('Código_interno', flat=True)
#------------------------------------------------------------------
#      Ejemplos de queries    ( de QuerySet API references )
#------------------------------------------------------------------
Tratamientos_ObrasSociales_Prepagas.objects.filter(Tratamiento__exact='Muelas').values().order_by('Obra_Social_Prepaga')
Tratamientos_ObrasSociales_Prepagas.objects.values_list('Tratamiento','Precio')
Tratamientos_ObrasSociales_Prepagas.objects.distinct()
qs1.union(qs2, qs3)
qs1.intersection(qs2, qs3)
select_related() #---Probar con presupuestos y pacientes

Tratamientos_ObrasSociales_Prepagas.objects.filter(Código__in=[1])
uno=Tratamientos_ObrasSociales_Prepagas.objects.filter(Tratamiento__exact='Encías').filter(Obra_Social_Prepaga__in=['Sancor'])
#---Operators that return new QuerySets---
#--Se pueden usar:
AND (&)
OR (|)
XOR (^)



#------------------------------------------------------------------
#      Carga rápida de datos
#------------------------------------------------------------------
pacientes = [
    Pacientes.objects.create(Nombre="Juan Fosch",DNI=30231654,Teléfono=261549874,E_mail='mail@mail.com',Obra_Social_Prepaga='Sancor'),
    Pacientes.objects.create(Nombre="Facundo Ortega",DNI=32489236,Teléfono=549261352,E_mail='mail@mail.com',Obra_Social_Prepaga='OSDE'),
    Pacientes.objects.create(Nombre="Paciente Ejmplo",DNI=28564789,Teléfono=262456987,E_mail='mail@mail.com',Obra_Social_Prepaga='Medifé'),
 ]
pacientes[0]
#Pacientes.objects.bulk_update(Pacientes, ["Nombre"])
tratamientos_propios=[
                    Tratamientos_Propios.objects.create(Código_interno=1, Tratamiento='Muelas'),
                    Tratamientos_Propios.objects.create(Código_interno=2, Tratamiento='Encías'),
                    Tratamientos_Propios.objects.create(Código_interno=3, Tratamiento='Implante'),
]


#------------------------------------------------------------------
#   Pruebas de queries
#------------------------------------------------------------------

Propios=Tratamientos_Propios.objects.get(Tratamiento='Muelas')
Otros=Tratamientos_ObrasSociales_Prepagas.objects.filter(Tratamiento__exact='Muelas').filter(Obra_Social_Prepaga__exact='Implante')
for valor in Otros:
    if valor.Obra_Social.Prepaga in
    print(valor.Obra_Social_Prepaga)

Presupuestos.objects.filter(Monto__exact=1000).values()
Presupuestos.objects.filter(Número_de_orden=1).values()
Presupuestos.objects.values_list('Monto')

# Este saca los números de comprobantes correspondientes al número de orden 2
compr=Cobranzas.objects.filter(Número_de_orden__exact=2).values_list('Número_de_comprobante',flat=True) 
for valor in compr:
    print(valor)
comprobantes=Cobranzas.objects.filter(Número_de_orden__exact=2).values_list('Número_de_comprobante','Cuánto_pagó')

# Este calcula el Saldo!
monto=Presupuestos.objects.filter(Número_de_orden__exact=2).values_list('Monto', flat=True)
cuánto_pagó=Cobranzas.objects.filter(Número_de_orden__exact=2).values_list('Cuánto_pagó', flat=True).aggregate(Sum("Cuánto_pagó")) 
saldo= monto[0] - cuánto_pagó['Cuánto_pagó__sum'] 
números_de_comprobante=Cobranzas.objects.filter(Número_de_orden__exact=2).values_list('Número_de_comprobante', flat=True)
for i in números_de_comprobante:
    compr=i
    compr
# Para trabajar con agregaciones en los QuerySet (contar, sumar, promedio, etc) hay que usar las funciones de cada tipo importadas desde Django.
# Para usar la función 'Sum' hay que importarla así: from django.db.models import Sum. 
Cobranzas.objects.aggregate(Sum("Cuánto_pagó"))
#------------------------------------------------------------------
#       Maneras de corroborar si hay que cobrar por obra social o particular
#------------------------------------------------------------------
Otros=Tratamientos_ObrasSociales_Prepagas.objects.all()
# Primera
obra_social_paciente=input('Qúe obra social tenés?: ')
tratamiento=input('Qué te vas a hacer: ')

for valor in Otros:
    #print(valor.Obra_Social_Prepaga)
    if valor.Obra_Social_Prepaga == f'{obra_social_paciente}' and valor.Tratamiento == f'{tratamiento}':
        print('está')
    else:
        print('no está')

# Segunda (Esta está bien)
pedido={'obra_social':[],'tratamiento':[]} # Hay que hacer listas dentro del diccionario porque el filtro '__in' trabaja con iterables.
obra_social_paciente=input('Qúe obra social tenés?: ')
pedido['obra_social'].append(obra_social_paciente) # Por eso se usa append acá, después hay que ver cómo hacer para que el diccionario 'pedido' quede vacío después.
                                                # Puede ser porque se renueva dentro de un bucle, o porque se se usa '.pop()'
tratamiento=input('Qué te vas a hacer: ')
pedido['tratamiento'].append(tratamiento)


Tratamientos_ObrasSociales_Prepagas.objects.filter(Código__in=[1])
consulta_tiene=Tratamientos_ObrasSociales_Prepagas.objects.filter(Tratamiento__in=pedido['tratamiento']).filter(Obra_Social_Prepaga__in=pedido['obra_social'])
consulta_no_tiene=Tratamientos_ObrasSociales_Prepagas.objects.filter(Tratamiento__exact='Encías').filter(Obra_Social_Prepaga__in=pedido)

for tratamiento_recibido in consulta_tiene.values_list('Tratamiento',flat=True):
    tratamiento_recibido=tratamiento_recibido

if tratamiento_recibido == pedido['tratamiento'][0] :
    print('Está')
else:
    print('No está')

#----------------------------------------------------------------------------------------


