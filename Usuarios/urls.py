"""Define los patrones URL para Usuarios."""

from django.urls import path, include

from . import views

app_name = 'Usuarios'
urlpatterns = [
    # Incluye las URL de autenticación predeterminadas.
    path('', include('django.contrib.auth.urls')), #--En lugar de llamar a un archivo de vistas con funciones, llama a la función de Django predeterminada.
    # Página de Registro
    path('Registro/', views.registro, name='registro'),
    ]