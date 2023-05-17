from django import forms
from .models import Pacientes, Presupuestos, Cobranzas


class PacientesForm(forms.ModelForm):
    class Meta:
        model = Pacientes
        fields = ['Nombre','DNI','Teléfono','E_mail','Obra_Social_Prepaga']
        labels = {'text': 'Paciente'}



class PresupuestosForm(forms.ModelForm):
    class Meta:
        model= Presupuestos
        fields =['Paciente_Dni','Número_de_orden','Tratamiento_1','Tratamiento_2','Tratamiento_3','Monto']
        labels = {'text': ''}

    def save(self, commit=True):
        fields_presu=super(PresupuestosForm,self).save(commit=False)

        if commit:
            fields_presu.save()
        return (fields_presu)


class CobranzasForm(forms.ModelForm):
    class Meta:
        model= Cobranzas
        fields =['Número_de_comprobante','Número_de_orden','Cuánto_pagó']
        labels = {'text': ''}

    def save(self, commit=True):
        fields_cobra=super(CobranzasForm,self).save(commit=False)

        if commit:
            fields_cobra.save()
        return (fields_cobra)