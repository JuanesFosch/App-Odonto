# Código que interactúa con el gestor de bases de datos MySQL. Para crear y/o modificar conexiones, bases de datos, tablas, registros. 
# También tiene las consultas para mostar en las GUI.


import mysql
from mysql import connector
from mysql.connector import Error



def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database= db_name
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

connection = create_connection("localhost", "root", "","app_odonto") #Llama a la función creada.

"""def create_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database created successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

create_database_query = "CREATE DATABASE App_Odonto"
create_database(connection, create_database_query) #Llama a la función creada."""

def execute_query(connection, query): # Ejecuta alguna consulta, activando la conexión y tomando la consulta a ejecutar.
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")
        pass

create_table = """    
CREATE TABLE IF NOT EXISTS presupuestos (
  Id INT AUTO_INCREMENT,
  DNI INT,
  Nombre TEXT, 
  Tratamiento TEXT NOT NULL, 
  Precio INT, 
  Forma_de_Pago INT, 
  Cuotas TEXT,
  PRIMARY KEY (id)
) """
# Está bien que se usen las comillas, aunque parezca anulado.

delete_table= """
DROP TABLE pacientes;
"""

def create_users(Nombre,DNI,Obra_Social_Prepaga,Tel,Mail,Historia,Código):
    cursor = connection.cursor()
    cursor.execute(
    "INSERT INTO pacientes (Nombre,DNI,Tel,Mail,Historia_clínica,Obra_Social_Prepaga,Código) VALUES (%s,%s,%s,%s,%s,%s,%s);",
    (Nombre,DNI,Obra_Social_Prepaga,Tel,Mail,Historia,Código))

#,Costo,Presupuesto,Tipo_de_Pago,Notas

def query_pacientes_dni(): # Trae los DNI de los pacientes.
    cursor = connection.cursor(buffered=True)
    cursor.execute("SELECT DNI FROM pacientes")
    resultado = cursor.fetchall()
    resultado_limpio=[x[0] for x in resultado] # Porque devolvía una lista con tuplas adentro y los nombres entre llaves. Al especificar el índice, los trae como string.
    
    return resultado_limpio

def query_id(valor):
 
    cursor = connection.cursor(buffered=True)
    cursor.execute(f"SELECT Id FROM pacientes WHERE DNI = {valor} or Nombre = {valor} ;" )
    #cursor.execute(sql,{'DNI': DNI})
    resultado = cursor.fetchall()
    resultado_limpio=[x[0] for x in resultado]
    #print(resultado)
    #print(resultado_limpio)
    return resultado_limpio
    
def query_nombre_id(id):
    cursor = connection.cursor(buffered=True)
    cursor.execute(f"SELECT Nombre FROM pacientes WHERE Id = {id};" )
    #cursor.execute(sql,{'DNI': DNI})
    resultado = cursor.fetchall()
    resultado_limpio=[x[0] for x in resultado]
    #print(resultado)
    #print(resultado_limpio)
    return resultado_limpio

def query_dni_id(id):
    cursor = connection.cursor(buffered=True)
    cursor.execute(f"SELECT DNI FROM pacientes WHERE Id = {id};" )
    #cursor.execute(sql,{'DNI': DNI})
    resultado = cursor.fetchall()
    resultado_limpio=[x[0] for x in resultado]
    #print(resultado)
    #print(resultado_limpio)
    return resultado_limpio

def query_pacientes_nombre(): # Trae los Nombres de los pacientes.
    cursor = connection.cursor(buffered=True)
    cursor.execute("SELECT Nombre FROM pacientes")
    resultado = cursor.fetchall()
    resultado_limpio=[x[0] for x in resultado] # Porque devolvía una lista con tuplas adentro y los nombres entre llaves. Al especificar el índice, los trae como string.
   
    return resultado_limpio

def query_info(event,value): # Trae el nombre, teléfono y mail de los pacientes.
    cursor = connection.cursor(buffered=True)
    cursor.execute(f"SELECT Nombre, Tel, Mail FROM pacientes WHERE Nombre = {value} or DNI = {value}") # El 'value'lo toma de la lista desplegable modificada con los DNI.

    result = cursor.fetchall()

    for row in result:
        consulta=row
 
    return consulta[0]+', '+str(consulta[1])+', '+consulta[2] 
#Acá probrar excepción de errores.

def query_historia(event,value): # Trae la hsitoria clínica de los pacientes.
    cursor = connection.cursor(buffered=True)
    cursor.execute(f"SELECT Historia_clínica FROM pacientes WHERE Nombre = {value} or DNI = {value} ") # El 'value'lo toma de la lista desplegable modificada con los DNI.

    result = cursor.fetchall()

    for row in result:
        consulta=row
 
    return consulta[0] # Se especifica el valor 0 de la tupla que se genera, para verlo como string.

""" 
def query_deuda(event,value):
    cursor = connection.cursor(buffered=True)
    cursor.execute(f"SELECT Historia_clínica FROM pacientes WHERE DNI = {value}") # El 'value'lo toma de la lista desplegable modificada con los DNI.

    result = cursor.fetchall()

    for row in result:
        consulta=row
 
    return consulta[0] # Se especifica el valor 0 de la tupla que se genera, para verlo como string.
""" # Falta generar el valor de la deuda del paciente, tomando algún valor que haya pagado y restándoselo al presupuesto.

def query_costo(event,value): # Trae el costo de los pacientes.
    cursor = connection.cursor(buffered=True)
    cursor.execute(f"SELECT Costo FROM pacientes WHERE Nombre = {value} or DNI = {value} ") # El 'value'lo toma de la lista desplegable modificada con los DNI.

    result = cursor.fetchall()
    
    for row in result:
        consulta=row
        #resultado_limpio=[x[0] for x in consulta]    
    return consulta[0] # Se especifica el valor 0 de la tupla que se genera, para verlo como string.

def query_presupuesto(event,value): # Trae el presupuesto de los pacientes.
    cursor = connection.cursor(buffered=True)
    cursor.execute(f"SELECT Presupuesto FROM pacientes WHERE Nombre = {value} or DNI = {value}") # El 'value'lo toma de la lista desplegable modificada con los DNI.

    result = cursor.fetchall()

    for row in result:
        consulta=row
 
    return consulta[0] # Se especifica el valor 0 de la tupla que se genera, para verlo como string.
 
def query_forma_de_pago(event,value): # Trae la forma de pago de los pacientes.
    cursor = connection.cursor(buffered=True)
    cursor.execute(f"SELECT Tipo_de_Pago FROM pacientes WHERE Nombre = {value} or DNI = {value}") # El 'value'lo toma de la lista desplegable modificada con los DNI.

    result = cursor.fetchall()

    for row in result:
        consulta=row
 
    return consulta[0] # Se especifica el valor 0 de la tupla que se genera, para verlo como string. 

#execute_query(connection, create_table)