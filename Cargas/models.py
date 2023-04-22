from django.db import models

# Create your models here.


class Pacientes(models.Model):
    Nombre= models.CharField(max_length=40)
    DNI= models.IntegerField(primary_key=True,default=0000)
    Teléfono = models.IntegerField()
    E_mail= models.CharField(max_length=40)
    Obra_Social_Prepaga= models.CharField(max_length=40)    # Esto se debería poder elegir de una lista.

    def __str__(self): 
        return self.Nombre + " - DNI: " + str(self.DNI)

    class Meta:
        verbose_name_plural= "Pacientes"
        ordering = ['Nombre']

        
class Presupuestos(models.Model):
    #consultar Nombre
    Paciente_Dni= models.ForeignKey("Pacientes",on_delete=models.CASCADE)
    Número_de_orden= models.IntegerField(primary_key=True,auto_created=True,default=0000)  # número de orden automático
    Fecha= models.DateField(auto_now_add=True,blank=True)
    # Tratamiento consultado a la lista de códigos
    Tratamiento_1= models.CharField(max_length=100,blank=True)  # Para tratamientos por particular
    Tratamiento_2= models.CharField(max_length=100,blank=True)  # Para tratamientos por particular  
    Tratamiento_3= models.CharField(max_length=100,blank=True)  # Para tratamientos por particular
    Monto = models.IntegerField(blank=True)
    #Forma de pago
    #Cuotas

    def __str__(self):
        return "Número de orden: " + str(self.Número_de_orden)

    class Meta:
        verbose_name_plural= "Presupuestos"
        ordering = ['Número_de_orden']     

class Cobranzas(models.Model):
    pass
 