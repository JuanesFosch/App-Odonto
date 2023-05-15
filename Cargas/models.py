from django.db import models




class Pacientes(models.Model):
    """Modelo que crea la tabla 'Cargas_pacientes' en la BD y la interacción en el sitio para ingresar datos."""
    Nombre= models.CharField(max_length=40, blank=False)
    DNI= models.IntegerField(primary_key=True,default=0000, blank=False)
    Teléfono = models.IntegerField(blank=False)
    E_mail= models.CharField(max_length=40)
    Obra_Social_Prepaga= models.CharField(max_length=40)    # Esto se debería poder elegir de una lista.

    def __str__(self):                                      # Formateo del modelo visible en la web
        return self.Nombre + " - DNI: " + str(self.DNI)

    class Meta:                                             # Formateo del modelo visible en la web
        verbose_name_plural= "Pacientes"
        ordering = ['Nombre']

        
class Presupuestos(models.Model):
    """Modelo que crea la tabla 'Cargas_presupuestos' en la BD y la interacción en el sitio para ingresar datos."""
    #consultar Nombre a la BD
    Paciente_Dni= models.ForeignKey("Pacientes",on_delete=models.CASCADE, related_name='Presupuestos')
    Número_de_orden= models.IntegerField(primary_key=True,auto_created=True,default=0000,blank=False)  
    Fecha= models.DateField(auto_now_add=True,blank=True)
    # Acá van campos con los tipos de tratamientos consultados a una futura tabla de códigos de las obras sociales y prepagas.
    # ------- 
    Tratamiento_1= models.CharField(max_length=100,blank=True)  # Para tratamientos por particular
    Tratamiento_2= models.CharField(max_length=100,blank=True)  # Para tratamientos por particular  
    Tratamiento_3= models.CharField(max_length=100,blank=True)  # Para tratamientos por particular
    Monto = models.IntegerField(blank=False)
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
    Número_de_orden= models.ManyToManyField(Presupuestos,blank=False,auto_created=True,related_name='Cobranzas')
    #DNI
    #NÚMERO DE TRATAMIENTO
    Fecha_de_cobro= models.DateField(auto_now_add=True,blank=True)
    Cuánto_pagó = models.IntegerField(blank=False)
    # Formateo del modelo visible en la web
    def __str__(self):                                          
        return "Número de comprobante: " + str(self.Número_de_comprobante)+" - Número_de_orden: " + str(self.Número_de_orden)
    
    # Formateo del modelo visible en la web
    class Meta:                                                 
        verbose_name_plural= "Cobranzas"
        ordering = ['Número_de_comprobante']

class Saldos(models.Model):
    """Modelo que crea la tabla Saldos"""
    Número_de_orden= models.ForeignKey("Presupuestos",on_delete=models.CASCADE,null=True)
    Monto= models.IntegerField(null=True) 
    Saldo= models.IntegerField(null=True)
    Cuánto_pagó=models.IntegerField(null=True)
    Número_de_comprobante= models.ForeignKey("Cobranzas",on_delete=models.CASCADE,null=True)

    def __str__(self):                                          
        return "Número de orden: " + str(self.Número_de_orden)+" - Saldo: " + str(self.Saldo)
    
    # Formateo del modelo visible en la web
    class Meta:                                                 
        verbose_name_plural= "Saldos"
        ordering = ['Número_de_orden']
    


    


    
 