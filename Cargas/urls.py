"""Define los patrones URL para Cargas."""

from django.urls import path

from . import views

app_name = 'Cargas'
urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    # Página que muestra todas las secciones para acceder
    path('secciones', views.secciones, name='secciones'),
    # Página con la sección 'Pacientes'
    path('pacientes', views.pacientes, name='pacientes'),
    # Página con la sección 'Carga de Pacientes'
    path('carga_pacientes', views.carga_pacientes, name='carga_pacientes'),
    # Página con la sección 'Presupuestos'
    path('presupuestos', views.presupuestos, name='presupuestos'),
    # Página con la sección 'Carga de Presupuestos'
    path('carga_presupuestos', views.carga_presupuestos, name='carga_presupuestos'),
    # Página con la sección 'Cobranzas'
    path('cobranzas', views.cobranzas, name='cobranzas'),
    # Página con la sección 'Carga de Cobranzas'
    path('carga_cobranzas', views.carga_cobranzas, name='carga_cobranzas'),
]   