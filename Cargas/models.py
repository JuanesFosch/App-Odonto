from django.db import models
from django.contrib.auth.models import User




class Pacientes(models.Model):
    """Modelo que crea la tabla 'Cargas_pacientes' en la BD y la interacción en el sitio para ingresar datos."""
    Nombre= models.CharField(max_length=40, blank=False)
    DNI= models.IntegerField(primary_key=True,default=0000, blank=False)
    Teléfono = models.IntegerField(blank=False)
    E_mail= models.CharField(max_length=40)
    Obra_Social_Prepaga= models.CharField(max_length=40)    # Esto se debería poder elegir de una lista.
    owner = models.ForeignKey(User, on_delete=models.CASCADE,default=1)

    def __str__(self):                                      # Formateo del modelo visible en la web
        return self.Nombre + " - DNI: " + str(self.DNI)

    class Meta:                                             # Formateo del modelo visible en la web
        verbose_name_plural= "Pacientes"
        ordering = ['Nombre']


class Tratamientos_Propios(models.Model):
    """Modelo que crea la tabla 'Cargas_Tratamientos_Propios' en la BD y la interacción en el sitio para ingresar datos."""
    Código_interno= models.IntegerField(null=False,default=0)
    Tratamiento= models.CharField(primary_key=True,max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE,default=1)

    def __str__(self):                                      
        return self.Tratamiento + " - " +str(self.Código_interno)

    class Meta:                                             # Formateo del modelo visible en la web
        verbose_name_plural= "Tratamientos Propios" 
        ordering = ['Código_interno']

class Tratamientos_ObrasSociales_Prepagas(models.Model):
    """Modelo que crea la tabla 'Cargas_Tratamientos_ObrasSociales_Prepagas' en la BD y la interacción en el sitio para ingresar datos."""
    Obra_Social_Prepaga= models.CharField(max_length=40)
    Tratamiento= models.CharField(max_length=50)
    Código= models.IntegerField(primary_key=True, default=0) #--Podría consultarse el código a la otra tabla
    Precio= models.IntegerField(null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    
    def __str__(self):                                      
        return self.Tratamiento + " - " +str(self.Obra_Social_Prepaga)

    class Meta:                                             # Formateo del modelo visible en la web
        verbose_name_plural= "Tratamientos Obras Sociales y Prepagas" 
        ordering = ['Tratamiento']
        
class Presupuestos(models.Model):
    """Modelo que crea la tabla 'Cargas_presupuestos' en la BD y la interacción en el sitio para ingresar datos."""
    #consultar Nombre a la BD
    Paciente_Dni= models.ForeignKey("Pacientes",on_delete=models.CASCADE, related_name='Presupuestos')
    Número_de_orden= models.IntegerField(primary_key=True,auto_created=True,default=0000,blank=False)  
    Fecha= models.DateField(auto_now_add=True,blank=True)
    # Acá van campos con los tipos de tratamientos consultados a la tabla de tratamientos propia.
    TRATAMIENTOS= ( 
            ('Muelas','Muelas'),
            ('Encías','Encías'),
            ('Implante','Implante')
        )
    # ------- 
    Tratamiento_1= models.CharField(max_length=100,blank=True,choices=TRATAMIENTOS)  # Para tratamientos por particular
    Tratamiento_2= models.CharField(max_length=100,blank=True,choices=TRATAMIENTOS)  # Para tratamientos por particular  
    Tratamiento_3= models.CharField(max_length=100,blank=True,choices=TRATAMIENTOS)  # Para tratamientos por particular
    # Acá una bandera que muestre si el tratamiento pasa por obra social o particular.
    Monto = models.IntegerField(blank=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    #Forma de pago
    #Cuotas

    def __str__(self):                                          # Formateo del modelo visible en la web
        return "Número de orden: " + str(self.Número_de_orden) 

    class Meta:                                                 # Formateo del modelo visible en la web
        verbose_name_plural= "Presupuestos"
        ordering = ['Número_de_orden']     

class Cobranzas(models.Model):
    """Modelo que crea la tabla 'Cargas_cobranzas' en la BD y la interacción en el sitio para ingresar datos."""
    Número_de_comprobante= models.IntegerField(primary_key=True,auto_created=True,default=0000)
    Número_de_orden= models.ManyToManyField(Presupuestos,blank=False,auto_created=True,related_name='Cobranzas', through='CobranzasPresupuestos_Inter')
    #DNI
    #NÚMERO DE TRATAMIENTO
    Fecha_de_cobro= models.DateField(auto_now_add=True,blank=True)
    Cuánto_pagó = models.IntegerField(blank=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    # Formateo del modelo visible en la web
    def __str__(self):                                          
        return "Número de comprobante: " + str(self.Número_de_comprobante)+" - Número_de_orden: " + str(self.Número_de_orden)
    
    # Formateo del modelo visible en la web
    class Meta:                                                 
        verbose_name_plural= "Cobranzas"
        ordering = ['Número_de_comprobante']


class CobranzasPresupuestos_Inter(models.Model):
    """Tabla intermedia para la relación muchos a muchos entre 'Cobranzas' y 'Presupuestos'."""
    cobranzas = models.ForeignKey(Cobranzas, on_delete=models.CASCADE)
    presupuesto = models.ForeignKey(Presupuestos, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=1)


    


    


    
 