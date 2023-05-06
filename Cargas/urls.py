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
    # Página con la sección 'Presupuestos'
    path('presupuestos', views.presupuestos, name='presupuestos'),
    # Página con la sección 'Cobranzas'
    path('cobranzas', views.cobranzas, name='cobranzas'),
]