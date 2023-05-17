from django.contrib import admin

# Register your models here.

from .models import Pacientes, Tratamientos_Propios, Tratamientos_ObrasSociales_Prepagas, Presupuestos,Cobranzas 
admin.site.register(Pacientes)
admin.site.register(Tratamientos_Propios)
admin.site.register(Tratamientos_ObrasSociales_Prepagas)
admin.site.register(Presupuestos)
admin.site.register(Cobranzas)


