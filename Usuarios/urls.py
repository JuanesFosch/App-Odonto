"""Define los patrones URL para Usuarios."""

from django.urls import path, include

from . import views

app_name = 'Usuarios'
urlpatterns = [
    # Incluye las URL de autenticación predeterminadas.
    #--En lugar de llamar a un archivo de vistas con funciones, llama a la función de Django predeterminada con todas las funciones para el manejo de usuarios.
    path('', include('django.contrib.auth.urls')), 
    # Página de Registro
    path('Registro/', views.registro, name='registro'),
    ]