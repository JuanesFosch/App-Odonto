# Código que genera una GUI para ingresar datos de presupuesto en una base de datos y en un archivo de Excel existentes.

import PySimpleGUI as sg
import App_Lolo_SQL

query_pacientes_dni= App_Lolo_SQL.query_pacientes_dni           # Trae los DNI de los pacientes.
query_pacientes_nombre= App_Lolo_SQL.query_pacientes_nombre     # Trae los Nombres de los pacientes.
query_id=App_Lolo_SQL.query_id                  # Trae el Id del registro según Nombre o DNI.
connection = App_Lolo_SQL.connection            # Parámetros de conexión a la base de datos.
execute_query = App_Lolo_SQL.execute_query      # Función para ejecutar alguna consulta SQL.
query_nombre_id=App_Lolo_SQL.query_nombre_id    # Trae el nombre del paciente según el Id consultado.
query_dni_id=App_Lolo_SQL.query_dni_id    # Trae el DNI del paciente según el Id consultado.
#-----------------------------Creación de la GUI-------------------------------------------------------------------------

#-------Carga de pacientes
formatos={'Letra':'Italic','Tamaño título':14,'Tamaño bloques':12}

presupuestos_col= [
                [sg.Text('Buscar por D.N.I',size=(20,1),font=(formatos['Letra'],formatos['Tamaño título']))], #Consultar DNI del paciente para cargarle un presupuesto.
                [sg.Combo(values=(query_pacientes_dni()),default_value='Seleccionar',size=(15,1),font=(formatos['Letra'][0],11),enable_events=True,key='-Lista DNI-')], 
                [sg.Text('Buscar por Nombre',size=(20,1),font=(formatos['Letra'],formatos['Tamaño título']))], # Consultar nombre del paciente para cargarle un presupuesto.
                [sg.Combo(values=(query_pacientes_nombre()),default_value='Seleccionar',size=(15,1),font=(formatos['Letra'][0],11),enable_events=True,key='-Lista NOM-')],  
                [sg.Text('DNI', size=(15,1),font=(formatos['Letra'],formatos['Tamaño bloques'])), sg.InputText(size=(30),key='-DNI-')],
                [sg.Text('Nombre', size=(15,1),font=(formatos['Letra'],formatos['Tamaño bloques'])), sg.InputText(size=(30),key='-Nombre-')],
                [sg.Text('Tratamiento', size=(15,1),font=(formatos['Letra'],formatos['Tamaño bloques'])), sg.InputText(size=(30),key='-TRA-')],
                [sg.Text('Precio', size=(15,1),font=(formatos['Letra'],formatos['Tamaño bloques'])), sg.InputText(size=(10),key='-PRECIO-')],
                [sg.Text('Forma de pago', size=(15,1),font=(formatos['Letra'],formatos['Tamaño bloques'])), sg.InputText(size=(10),key='-PAGO-')],
                [sg.Text('Cuotas', size=(15,1),font=(formatos['Letra'],formatos['Tamaño bloques'])), sg.InputText(size=(10),key='-CUOTAS-')]
                ]



layout_carga_presupuesto = [
    [sg.Text('Cargar presupuesto a:',font=(formatos['Letra'],formatos['Tamaño título']))],
    [sg.Column(presupuestos_col,element_justification='l',vertical_alignment='t',grab=True)],
    [sg.Submit('Cargar'), sg.Button('Limpiar'), sg.Exit('Salir',key='-SALIR-')]
    ]

window_presupuestos = sg.Window('Odonto', layout=layout_carga_presupuesto) 

#------------------------------------Bucle de eventos---------------------------------------------------------------
def clear_input():
    for key in values:
        window_presupuestos[key]('') #Pone una string vacía en el lugar donde había otra. Identifica el lugar por la 'key'.
    return None

while True:
    event, values = window_presupuestos.read() # Toma los 'event' y 'values' de la 'window' (según los parámetros de la función "read()"). En este caso son los event y values del 'layout' creado.
    dni_pac=query_pacientes_dni() # Trae los DNI de los pacientes.
    nombre_pacientes= query_pacientes_nombre() # Trae los Nombres de los pacientes.
    #nombre_por_id= query_nombre() #Trae los nombres de los pacientes según el Id.

    window_presupuestos['-Lista NOM-'].update(values=nombre_pacientes)
    window_presupuestos['-Lista DNI-'].update(values=dni_pac)
    if event == sg.WIN_CLOSED or event == '-SALIR-':
        break
    if event == '-Lista DNI-':
        dni_unico=(values['-Lista DNI-'])
        window_presupuestos['-DNI-'].update(dni_unico)

        new_dni = query_id(dni_unico) # Le pasa el valor del DNI a la función para que traiga el Id.    

        nombre_id= query_nombre_id(new_dni[0]) # Trae el nombre del paciente según el Id relacionado con el DNI.
        #print(nombre_id[0])
        # Actualización de los valores en los cuadros y listas.
        window_presupuestos['-Nombre-'].update(nombre_id[0])
        window_presupuestos['-Lista DNI-'].update(dni_unico)    
        window_presupuestos['-Lista NOM-'].update(nombre_id[0])

    if event == '-Lista NOM-':
        nombre_prolijo=(values['-Lista NOM-']) # Venía entre llaves.
        nombre=f'"{nombre_prolijo}"'   # Limpia el texto para pasarlo a la función.
        
        nuevo_nombre= query_id(nombre)  # Le pasa el valor del Nombre a la función para que traiga el Id.
        
        dni_id=query_dni_id(nuevo_nombre[0])  # Trae el DNI del paciente según el Id relacionado con el Nombre.
        # Actualización de los valores en los cuadros y listas.
        window_presupuestos['-Nombre-'].update(nombre_prolijo) 
        window_presupuestos['-DNI-'].update(dni_id[0])
        window_presupuestos['-Lista DNI-'].update(dni_id[0])
        window_presupuestos['-Lista NOM-'].update(nombre_prolijo)

    if event == 'Limpiar':
        clear_input()
        window_presupuestos['-Lista DNI-'].update('Seleccionar')
        window_presupuestos['-Lista NOM-'].update('Seleccionar')


