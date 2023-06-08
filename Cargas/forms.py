from django import forms
from .models import Pacientes, Presupuestos, Cobranzas, CobranzasPresupuestos_Inter, Tratamientos_Propios, Tratamientos_ObrasSociales_Prepagas


class PacientesForm(forms.ModelForm):
    """Plantilla para cargar un paciente"""
    class Meta:
        model = Pacientes
        fields = ['Nombre','DNI','Teléfono','E_mail','Obra_Social_Prepaga']
        labels = {'text': ''} # Esto transforma a la lista 'fields' en diccionario.


    
class PresupuestosForm(forms.ModelForm):
    """Plantilla para cargar un presupuesto"""
    class Meta:
        model= Presupuestos
        fields =['Número_de_orden','Tratamiento_1','Tratamiento_2','Tratamiento_3','Monto']
        labels = {'text': ''} # Esto transforma a la lista 'fields' en diccionario.

    def __init__(self, owner ,*args, **kwargs):
        super(PresupuestosForm, self).__init__(*args, **kwargs)

        # Filtrar las opciones del Paciente_Dni según el usuario actual
        pacientes_usuario = Pacientes.objects.filter(owner=owner).values_list('DNI', flat=True)
        self.fields['Paciente_Dni'] = forms.ModelChoiceField(queryset=pacientes_usuario) # Se agrega el par llave-valor 'Paciente_Dni' al diccionario 'fields'
        # Crear el próximo número de orden disponible
        presu_actual=Presupuestos.objects.values_list('Número_de_orden', flat=True).last()
        presu_actual += 1
        self.fields['Número_de_orden'] = forms.IntegerField(initial=presu_actual) # Se modifica el par llave-valor 'Número de orden' del diccionario 'fields'
           
        # Buscar los tratamientos para elegir
        tratamientos_propios= Tratamientos_Propios.objects.filter(owner=owner).values_list('Tratamiento', flat=True)
        propios_selección=[(item, item) for item in tratamientos_propios]
        propios_selección.append(('',''))
        propios_selección=tuple(propios_selección)
        self.fields['Tratamiento_1'] = forms.ChoiceField(choices=propios_selección,required=False)
        self.fields['Tratamiento_2'] = forms.ChoiceField(choices=propios_selección,required=False)
        self.fields['Tratamiento_3'] = forms.ChoiceField(choices=propios_selección,required=False)


    def save(self, commit=True):
        # Se toman los campos de la plantilla para cargar en la tabla 'Presupuestos'
        fields_presu=super(PresupuestosForm,self).save(commit=False)

        # Se crea una instancia del modelo "Pacientes" según el DNI seleccionado, para poder cargar un presupuesto a ese paciente.
        paciente_dni = self.cleaned_data['Paciente_Dni']
        paciente = Pacientes.objects.get(DNI=paciente_dni)
        fields_presu.Paciente_Dni = paciente

        if commit:
            fields_presu.save()
        return (fields_presu)

        
class Presupuestos_Os_Prepagas_Form(forms.ModelForm):
    """Plantilla para cargar un presupuesto"""
    class Meta:
        model= Presupuestos
        fields =['Número_de_orden','Tratamiento_1','Tratamiento_2','Tratamiento_3','Monto']
        labels = {'text': ''} # Esto transforma a la lista 'fields' en diccionario.

    def __init__(self, owner,*args, **kwargs):
        super(Presupuestos_Os_Prepagas_Form, self).__init__(*args, **kwargs)
        
        # Filtrar las opciones del Paciente_Dni según el usuario actual
        pacientes_usuario = Pacientes.objects.filter(owner=owner).values_list('DNI', flat=True)
        self.fields['Paciente_Dni'] = forms.ModelChoiceField(queryset=pacientes_usuario) # Se agrega el par llave-valor 'Paciente_Dni' al diccionario 'fields'
        
        #---------Los próximos campos se van a agregar después, porque hay que modificar el modelo Presupuestos----
        #os_prepagas=Tratamientos_ObrasSociales_Prepagas.objects.filter().values_list('Obra_Social_Prepaga', flat=True)
        #self.fields['Obra_Social_Prepaga']= forms.ModelChoiceField(queryset=os_prepagas)
        #código_os_prepagas= Tratamientos_ObrasSociales_Prepagas.objects.filter().values_list('Código', flat=True) 
        #self.fields['Código_tratamiento_Os_Prepaga']= forms.ModelChoiceField(queryset=código_os_prepagas)
        #código_interno= Tratamientos_Propios.objects.filter().values_list('Código_interno', flat=True) 
        #self.fields['Código_tratamiento_interno']= forms.ModelChoiceField(queryset=código_interno)
        #--------------------------------------------------------------------------------------------------------------
        
        # Crear el próximo número de orden disponible
        presu_actual=Presupuestos.objects.values_list('Número_de_orden', flat=True).last()
        presu_actual += 1
        self.fields['Número_de_orden'] = forms.IntegerField(initial=presu_actual) # Se modifica el par llave-valor 'Número de orden' del diccionario 'fields'
        self.fields['Tratamiento_1'] = forms.CharField(required=False)
        self.fields['Tratamiento_2'] = forms.CharField(required=False)
        self.fields['Tratamiento_3'] = forms.CharField(required=False)

    def save(self, commit=True):
        # Se toman los campos de la plantilla para cargar en la tabla 'Presupuestos'
        fields_presu_os_prepagas=super(Presupuestos_Os_Prepagas_Form,self).save(commit=False)

        # Se crea una instancia del modelo "Pacientes" según el DNI seleccionado, para poder cargar un presupuesto a ese paciente.
        paciente_dni = self.cleaned_data['Paciente_Dni']
        paciente = Pacientes.objects.get(DNI=paciente_dni)
        fields_presu_os_prepagas.Paciente_Dni = paciente

        if commit:
            fields_presu_os_prepagas.save()
        return (fields_presu_os_prepagas)


class CobranzasForm(forms.ModelForm):
    """Plantilla para cargar una cobranza"""
    class Meta:
        model= Cobranzas
        fields =['Número_de_comprobante','Número_de_orden','Cuánto_pagó']
        labels = {'text': ''}

    def __init__(self, owner,*args, **kwargs):
        super(CobranzasForm, self).__init__(*args, **kwargs)
        
        # Filtrar las opciones del Número_de_orden según el usuario actual
        user_specific_choices = Presupuestos.objects.filter(owner=owner).values_list('Número_de_orden', flat=True)
        self.fields['Número_de_orden'] = forms.ModelChoiceField(queryset=user_specific_choices)
        # Crear el próximo número de comprobante disponible
        comprob_actual=Cobranzas.objects.values_list('Número_de_comprobante', flat=True).last()
        comprob_actual += 1
        self.fields['Número_de_comprobante'] = forms.IntegerField(initial=comprob_actual) # Se modifica el par llave-valor 'Número de comprobante' del diccionario 'fields'
              
    def save(self,editar_cobranza_activa=False,commit=True): 
        # Se toman los campos de la plantilla para cargar en la tabla 'Cobranzas', y a su vez en la tabla intermedia 'CobranzasPresupuestos_Inter' 
        # de la relación Muchos a Muchos, para que se pueda reflejar el estado del presupuesto (Saldo y Números de comprobante correspondientes)
        fields_cobra=super(CobranzasForm,self).save(commit=False)   
        
        
        # Se crea una instancia de la tabla intermedia.
        intermedia= CobranzasPresupuestos_Inter()

        if editar_cobranza_activa == False:    # Si sólo se va a editar un registro en Cobranzas, no quiero que se agregue nada a la tabla intermedia, porque genera duplicados.
            intermedia.cobranzas = fields_cobra  # Como se va a agregar un registro a Cobranzas, se permite que la tabla intermedia también lo haga.
        
        # Se toma el número de orden para igualarlo al de la tabla intermedia, para posterior carga (se evitan duplicados).
        num_orden = self.cleaned_data['Número_de_orden']
        presupuesto_id_inter = Presupuestos.objects.get(Número_de_orden=num_orden)
        intermedia.presupuesto = presupuesto_id_inter
        
        #---CONDICIÓN DE QUE SI ESTA ACTIVA LA FUNCION EDITAR COBRANZAS, QUE NO CARGE NADA A LA TABLA INTERMEDIA
        if commit:
            fields_cobra.save()
            if editar_cobranza_activa == False: 
                intermedia.save()
        return (fields_cobra)

class TratamientosPropiosForm(forms.ModelForm):
    """Plantilla para cargar un tratamiento propio"""
    class Meta:
        model = Tratamientos_Propios
        fields = ['Código_interno','Tratamiento']
        labels = {'text': ''} # Esto transforma a la lista 'fields' en diccionario.

    def __init__(self, owner, *args, **kwargs):
        super(TratamientosPropiosForm, self).__init__(*args, **kwargs)

        # Crear el próximo código disponible
        código_actual = Tratamientos_Propios.objects.values_list('Código_interno', flat=True).last()
        código_actual += 1
        self.fields['Código_interno'] = forms.IntegerField(initial=código_actual) # Se modifica el par llave-valor 'Código interno' del diccionario 'fields'
       
    
    def save(self, commit=True): 
        # Se toman los campos de la plantilla para cargar en la tabla 'Tratamientos_Propios'
        # de la relación Muchos a Muchos, para que se pueda reflejar el estado del presupuesto (Saldo y Números de comprobante correspondientes)
        fields_propios=super(TratamientosPropiosForm,self).save(commit=False) 
        
        if commit:
            fields_propios.save()

        return (fields_propios)

class TratamientosOs_PrepagasForm(forms.ModelForm):
    """Plantilla para cargar un tratamiento propio"""
    class Meta:
        model = Tratamientos_ObrasSociales_Prepagas
        fields = ['Obra_Social_Prepaga','Tratamiento','Código','Precio']
        labels = {'text': ''} # Esto transforma a la lista 'fields' en diccionario.

    def __init__(self, owner, *args, **kwargs):
        super(TratamientosOs_PrepagasForm, self).__init__(*args, **kwargs)

        # Crear el próximo código disponible
        #código_actual = Tratamientos_ObrasSociales_Prepagas.objects.values_list('Código', flat=True).last()
        #código_actual += 1
        #self.fields['Código'] = forms.IntegerField(initial=código_actual) # Se modifica el par llave-valor 'Código interno' del diccionario 'fields'
        
    def save(self, commit=True): 
        # Se toman los campos de la plantilla para cargar en la tabla 'Tratamientos_Propios'
        fields_os_prepagas=super(TratamientosOs_PrepagasForm,self).save(commit=False) 
        
        if commit:
            fields_os_prepagas.save()

        return (fields_os_prepagas)