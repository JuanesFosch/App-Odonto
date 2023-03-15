# Código que genera una GUI para ingresar datos en un archivo de Excel EXISTENTE.

import PySimpleGUI as sg
import mysql
from mysql import connector
from mysql.connector import Error

#-----------------------------Trabajo con la GUI-------------------------------------------------------------------------

formatos={'Letra':'Italic','Tamaño título':14,'Tamaño bloques':12}

pacientes_col= [[sg.Text('Datos de Contacto:', size=(15,1),font=(formatos['Letra'],formatos['Tamaño título']))],
    [sg.Text('Nombre', size=(15,1),font='Verdana 12'), sg.InputText(key='-Nombre-')],
    [sg.Text('DNI', size=(15,1),font=(formatos['Letra'],formatos['Tamaño bloques'])), sg.InputText(key='-DNI-')],
    [sg.Text('Teléfono', size=(15,1),font=(formatos['Letra'],formatos['Tamaño bloques'])), sg.InputText(key='-Tel-')],
    [sg.Text('E-Mail', size=(15,1),font=(formatos['Letra'],formatos['Tamaño bloques'])), sg.InputText(key='-Mail-')],
    [sg.Text('Historia Clínica', size=(15,1),font=(formatos['Letra'],formatos['Tamaño bloques'])), sg.Multiline(default_text='-->',size=(45,5),key='-Historia-')]
    ]

OS_Prepaga_col= [
    [sg.Text('Obra Social/Prepaga:', size=(18,1),font=(formatos['Letra'],formatos['Tamaño título']))],
    [sg.Text('Obra Social/Prepaga', size=(18,1),font=(formatos['Letra'],formatos['Tamaño bloques'])), sg.InputText(size=(15,1),key='-Obra Social/Prepaga-')], #Esto va en otra columna
    [sg.Text('Código de Prestación', size=(18,1),font=(formatos['Letra'],formatos['Tamaño bloques'])), sg.InputText(size=(15,1),key='-Código-')], #Esto va en otra columna
    ]

Cobro_col=[
    [sg.Text('Cobranza:', size=(10,1),font=(formatos['Letra'],formatos['Tamaño título']))],
    [sg.Text('Costo', size=(10,1),font=(formatos['Letra'],formatos['Tamaño bloques'])), sg.InputText(pad=(21,1),size=(15,1),default_text='$',key='-Costo-')], #Esto va en otra columna
    [sg.Text('Presupuesto', size=(10,1),font=(formatos['Letra'],formatos['Tamaño bloques'])), sg.InputText(pad=(21,1),size=(15,1),default_text='$',key='-Presupuesto-')], #Esto va en otra columna
    [sg.Text('Forma de Pago', size=(12,1),font=(formatos['Letra'],formatos['Tamaño bloques'])), sg.InputText(pad=(1,1),size=(15,1),key='-Pago-')],
    [sg.Text('Notas', size=(5,1),font=(formatos['Letra'],formatos['Tamaño bloques'])), sg.Multiline(pad=(70.5,1),size=(30,5),key='-Notas-')] #Esto va en otra columna
    ]

layout_pacientes = [
    [sg.Text('Carga de pacientes:',font=(formatos['Letra'],formatos['Tamaño título']))],
    [sg.Column(pacientes_col,element_justification='l',vertical_alignment='t',grab=True), 
    sg.VerticalSeparator(),
    sg.Column(OS_Prepaga_col,element_justification='l',vertical_alignment='t',grab=True),
    sg.VerticalSeparator(),
    sg.Column(Cobro_col,element_justification='l',vertical_alignment='t',grab=True)],
    [sg.Submit('Cargar'), sg.Button('Limpiar'), sg.Exit()]
    ]

window_pacientes = sg.Window('Odonto', layout=layout_pacientes)

#-----------------------------Trabajo con la Base de Datos-------------------------------------------------------------------------

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

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


def create_users(Nombre,DNI,Obra_Social_Prepaga,Tel,Mail,Historia,Código,Costo,Presupuesto,Pago,Notas):
    cursor = connection.cursor()
    cursor.execute(
    "INSERT INTO pacientes (Nombre,DNI,Obra_Social_Prepaga,Tel,Mail,Historia_clínica,Código,Costo,Presupuesto,Tipo_de_Pago,Notas) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);",
    (Nombre,DNI,Obra_Social_Prepaga,Tel,Mail,Historia,Código,Costo,Presupuesto,Pago,Notas))


#execute_query(connection, create_table)

#------------------------------------Bucle de eventos---------------------------------------------------------------

"""Para cargar los datos, hay que matchear el formato de INSERT de SQL con el código. Podría ser con un diccionario que se va llenando según los input.
    O buscar alguna función directa entre PySimpleGUI con SQL"""

def clear_input():
    for key in values:
        window_pacientes[key]('') #Pone una string vacía en el lugar donde había otra. Identifica el lugar por la 'key'.
    return None

while True:
    event, values = window_pacientes.read() # Toma los 'event' y 'values' de la 'window' (según los parámetros de la función). En este caso son los event y values del 'layout' creado.
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Limpiar':
        clear_input()
    if event == 'Cargar':
        new_record = execute_query(connection, create_users(values['-Nombre-'],values['-DNI-'],values['-Tel-'],values['-Mail-'],values['-Historia-'],
        values['-Obra Social/Prepaga-'],values['-Código-'],
        values['-Costo-'],values['-Presupuesto-'],values['-Pago-'],values['-Notas-'])) # Escribe datos nuevos.
        sg.popup('Datos guardados!')
        clear_input()
window_pacientes.close()