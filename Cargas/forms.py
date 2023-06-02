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

    def __init__(self, owner, *args, **kwargs):
        super(PresupuestosForm, self).__init__(*args, **kwargs)

        # Filtrar las opciones del Paciente_Dni según el usuario actual
        user_specific_choices = Pacientes.objects.filter(owner=owner).values_list('DNI', flat=True)
        self.fields['Paciente_Dni'] = forms.ModelChoiceField(queryset=user_specific_choices) # Se agrega el par llave-valor 'Paciente_Dni' al diccionario 'fields'
        # Crear el próximo número de orden disponible
        presu_actual=Presupuestos.objects.values_list('Número_de_orden', flat=True).last()
        presu_actual += 1
        self.fields['Número_de_orden'] = forms.IntegerField(initial=presu_actual) # Se modifica el par llave-valor 'Número de orden' del diccionario 'fields'

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


class CobranzasForm(forms.ModelForm):
    """Plantilla para cargar una cobranza"""
    class Meta:
        model= Cobranzas
        fields =['Número_de_comprobante','Número_de_orden','Cuánto_pagó']
        labels = {'text': ''}

    def __init__(self, owner, *args, **kwargs):
        super(CobranzasForm, self).__init__(*args, **kwargs)
        
        # Filtrar las opciones del Número_de_orden según el usuario actual
        user_specific_choices = Presupuestos.objects.filter(owner=owner).values_list('Número_de_orden', flat=True)
        self.fields['Número_de_orden'] = forms.ModelChoiceField(queryset=user_specific_choices)
        # Crear el próximo número de comprobante disponible
        comprob_actual=Cobranzas.objects.values_list('Número_de_comprobante', flat=True).last()
        comprob_actual += 1
        self.fields['Número_de_comprobante'] = forms.IntegerField(initial=comprob_actual) # Se modifica el par llave-valor 'Número de comprobante' del diccionario 'fields'

    def save(self, commit=True): 
        # Se toman los campos de la plantilla para cargar en la tabla 'Cobranzas', y a su vez en la tabla intermedia 'CobranzasPresupuestos_Inter' 
        # de la relación Muchos a Muchos, para que se pueda reflejar el estado del presupuesto (Saldo y Números de comprobante correspondientes)
        fields_cobra=super(CobranzasForm,self).save(commit=False)   
        
        intermedia= CobranzasPresupuestos_Inter()
        intermedia.cobranzas = fields_cobra
        num_orden = self.cleaned_data['Número_de_orden']
        presupuesto_instance = Presupuestos.objects.get(Número_de_orden=num_orden)
        intermedia.presupuesto = presupuesto_instance
        
        if commit:
            fields_cobra.save()
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
        # de la relación Muchos a Muchos, para que se pueda reflejar el estado del presupuesto (Saldo y Números de comprobante correspondientes)
        fields_os_prepagas=super(TratamientosOs_PrepagasForm,self).save(commit=False) 
        
        if commit:
            fields_os_prepagas.save()

        return (fields_os_prepagas)