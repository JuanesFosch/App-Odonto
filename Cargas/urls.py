"""Define los patrones URL para Cargas."""

from django.urls import path

from . import views

app_name = 'Cargas'
urlpatterns = [
    # Página inicial
    path('', views.index, name='index'),

    # Página que muestra todas las secciones para acceder
    path('secciones', views.secciones, name='secciones'),

    # Página con la sección 'Carga de Pacientes'
    path('carga_pacientes', views.carga_pacientes, name='carga_pacientes'),

    # Página con la sección 'Pacientes'
    path('pacientes', views.pacientes, name='pacientes'),

    # Página con la sección 'Editar Pacientes'
    path('editar_pacientes/<int:dni>/', views.editar_pacientes, name='editar_pacientes'),

    # Página con la sección 'Carga de Presupuestos'
    path('carga_presupuestos', views.carga_presupuestos, name='carga_presupuestos'),

    # Página con la sección 'Carga de Cobranzas'
    path('carga_cobranzas', views.carga_cobranzas, name='carga_cobranzas'),

    # Página con las secciones 'Presupuestos y Cobranzas'
    path('presupuestos_y_cobranzas', views.presupuestos_y_cobranzas, name='presupuestos_y_cobranzas'),

    # Página con la sección 'Editar Presupuestos'
    path('editar_presupuestos/<int:orden>/', views.editar_presupuestos, name='editar_presupuestos'),

    # Página con la sección 'Editar Cobranzas'
    path('editar_cobranzas/<int:comprobante>', views.editar_cobranzas, name='editar_cobranzas'),

    # Página con la sección 'Carga de Tratamientos'
    path('carga_tratamientos_propios', views.carga_tratamientos_propios, name='carga_tratamientos_propios'),

    # Página con la sección 'Carga de Tratamientos de Obras Sociales y Prepagas'
    path('carga_tratamientos_os_prepagas', views.carga_tratamientos_os_prepagas, name='carga_tratamientos_os_prepagas'),

    # Página con la sección 'Tratamientos'
    path('tratamientos', views.tratamientos, name='tratamientos'),

    # Página con la sección 'Editar Tratamientos Propios'
    path('editar_tratamientos_propios/<int:código>', views.editar_tratamientos_propios, name='editar_tratamientos_propios'),
    
    # Página con la sección 'Editar Tratamientos de Obras Sociales y Prepagas'
    path('editar_tratamientos_os_prepagas/<int:código>', views.editar_tratamientos_os_prepagas, name='editar_tratamientos_os_prepagas'),
    
]   


# Página de prueba para mostrar imágenes.
    #path('imagen', views.prueba_imagen, name='imagen'),