from django import forms
from .models import Pacientes, Presupuestos, Cobranzas, CobranzasPresupuestos_Inter


class PacientesForm(forms.ModelForm):
    class Meta:
        model = Pacientes
        fields = ['Nombre','DNI','Teléfono','E_mail','Obra_Social_Prepaga']
        labels = {'text': ''}



class PresupuestosForm(forms.ModelForm):
    class Meta:

        model= Presupuestos
        fields =['Número_de_orden','Tratamiento_1','Tratamiento_2','Tratamiento_3','Monto']
        labels = {'text': ''} # Esto transforma a la lista 'fields' en diccionario.

    def __init__(self, owner, *args, **kwargs):
        super(PresupuestosForm, self).__init__(*args, **kwargs)

        # Filtrar las opciones del Paciente_Dni según el usuario actual
        user_specific_choices = Pacientes.objects.filter(owner=owner).values_list('DNI', flat=True)
        self.fields['Paciente_Dni'] = forms.ModelChoiceField(queryset=user_specific_choices)
        presu_actual=Presupuestos.objects.values_list('Número_de_orden', flat=True).last()
        presu_actual += 1
        self.fields['Número_de_orden'] = forms.IntegerField(initial=presu_actual)

    def save(self, commit=True):
        fields_presu=super(PresupuestosForm,self).save(commit=False)
        print(type(self.fields))
        # Obtén la instancia de "Pacientes" según el DNI seleccionado

        paciente_dni = self.cleaned_data['Paciente_Dni']
        paciente = Pacientes.objects.get(DNI=paciente_dni)
        fields_presu.Paciente_Dni = paciente

        if commit:
            fields_presu.save()
        print(type(self.fields))
        return (fields_presu)


class CobranzasForm(forms.ModelForm):
    class Meta:
        model= Cobranzas
        fields =['Número_de_comprobante','Número_de_orden','Cuánto_pagó']
        labels = {'text': ''}

    def __init__(self, owner, *args, **kwargs):
        super(CobranzasForm, self).__init__(*args, **kwargs)
        
        # Filtrar las opciones del Número_de_orden según el usuario actual
        user_specific_choices = Presupuestos.objects.filter(owner=owner).values_list('Número_de_orden', flat=True)
        self.fields['Número_de_orden'] = forms.ModelChoiceField(queryset=user_specific_choices)
        comprob_actual=Cobranzas.objects.values_list('Número_de_comprobante', flat=True).last()
        comprob_actual += 1
        self.fields['Número_de_comprobante'] = forms.IntegerField(initial=comprob_actual)



    def save(self, commit=True): 
        # Se toman los campos del form para cargar en la tabla 'Cobranzas', y a su vez en la tabla intermedia 'CobranzasPresupuestos_Inter' 
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

        
