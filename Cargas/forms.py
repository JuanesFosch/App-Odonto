from django import forms
from .models import Pacientes, Presupuestos, Cobranzas, Saldos


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
        saldos_monto_y_saldo=Saldos(Número_de_orden_id=self.cleaned_data['Número_de_orden'],
                            Monto=self.cleaned_data['Monto'],
                            Saldo=self.cleaned_data['Monto'])

        if commit:
            fields_presu.save()
            saldos_monto_y_saldo.save()

        return (fields_presu, saldos_monto_y_saldo)


class CobranzasForm(forms.ModelForm):
    class Meta:
        model= Cobranzas
        fields =['Número_de_comprobante','Número_de_orden','Cuánto_pagó']
        labels = {'text': ''}

    def save(self, commit=True):
        fields_cobra=super(CobranzasForm,self).save(commit=False)
        saldos_comprobante_y_cuánto=Saldos(
                            Número_de_comprobante_id=self.cleaned_data['Número_de_comprobante'],
                            Número_de_orden_id=self.cleaned_data['Número_de_orden'],
                            Cuánto_pagó=self.cleaned_data['Cuánto_pagó'],
                            )

        if commit:
            fields_cobra.save()
            saldos_comprobante_y_cuánto.save()

        return (fields_cobra, saldos_comprobante_y_cuánto)