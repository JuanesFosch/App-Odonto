from django import forms
from .models import Pacientes, Presupuestos, Cobranzas, CobranzasPresupuestos_Inter, Tratamientos_Propios, Tratamientos_ObrasSociales_Prepagas

from Cargas.models import Pacientes, Presupuestos, Cobranzas, CobranzasPresupuestos_Inter, Tratamientos_Propios, Tratamientos_ObrasSociales_Prepagas



class Presupuestos_Os_Prepagas_Form(forms.ModelForm):
    """Plantilla para cargar un presupuesto"""
    class Meta:
        model= Presupuestos
        fields =['Número_de_orden','Tratamiento_1','Tratamiento_2','Tratamiento_3','Monto']
        labels = {'text': ''} # Esto transforma a la lista 'fields' en diccionario.
    def __init__(self, owner ,*args, **kwargs):
        super(Presupuestos_Os_Prepagas_Form, self).__init__(*args, **kwargs)
        # Filtrar las opciones del Paciente_Dni según el usuario actual
        pacientes_usuario = Pacientes.objects.filter(owner=owner).values_list('DNI', flat=True)
        self.fields['Paciente_Dni'] = forms.ModelChoiceField(queryset=pacientes_usuario) # Se agrega el par llave-valor 'Paciente_Dni' al diccionario 'fields'
        # Crear el próximo número de orden disponible
        presu_actual=Presupuestos.objects.values_list('Número_de_orden', flat=True).last()
        presu_actual += 1
        self.fields['Número_de_orden'] = forms.IntegerField(initial=presu_actual) # Se modifica el par llave-valor 'Número de orden' del diccionario 'fields'
    def clean(self):
        cleaned_data = super().clean()
        paciente_dni = cleaned_data.get('Paciente_Dni')
        # Hacer algo con el valor seleccionado
        
        #os_prepaga_paciente=Pacientes.objects.filter(DNI=32489236).values_list('Obra_Social_Prepaga', flat=True)   
        #dni = self.cleaned_data['Paciente_Dni']
        #print(dni)
        os_prepaga_paciente= Pacientes.objects.filter(DNI=paciente_dni).values_list('Obra_Social_Prepaga', flat=True)   
        # Buscar los tratamientos para elegir
        #Tratamientos_ObrasSociales_Prepagas.objects.filter(Obra_Social_Prepaga='OSDE').values_list('Tratamiento', flat=True)
        tratamientos_os_prepagas= Tratamientos_ObrasSociales_Prepagas.objects.filter(Obra_Social_Prepaga=os_prepaga_paciente[0]).values_list('Tratamiento', flat=True)
        os_prepagas_selección=[(item, item) for item in tratamientos_os_prepagas]
        os_prepagas_selección.append(('',''))
        os_prepagas_selección=tuple(os_prepagas_selección)
        self.fields['Tratamiento_1'] = forms.ChoiceField(choices=os_prepagas_selección,required=False)
        self.fields['Tratamiento_2'] = forms.ChoiceField(choices=os_prepagas_selección,required=False)
        self.fields['Tratamiento_3'] = forms.ChoiceField(choices=os_prepagas_selección,required=False)
        #Monto
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