from django.contrib import admin

# Register your models here.

from .models import Pacientes, Presupuestos, Cobranzas

admin.site.register(Pacientes)
admin.site.register(Presupuestos)
admin.site.register(Cobranzas)


