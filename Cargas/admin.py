from django.contrib import admin

# Register your models here.

from .models import Pacientes, Presupuestos, Cobranzas, Saldos

admin.site.register(Pacientes)
admin.site.register(Presupuestos)
admin.site.register(Cobranzas)
admin.site.register(Saldos)


