# Código que genera una GUI para ingresar datos de presupuesto en una base de datos y en un archivo de Excel existentes.

import PySimpleGUI as sg
import App_Odonto_SQL

query_pacientes_dni= App_Odonto_SQL.query_pacientes_dni           # Trae los DNI de los pacientes.
query_pacientes_nombre= App_Odonto_SQL.query_pacientes_nombre     # Trae los Nombres de los pacientes.
#query_id=App_Odonto_SQL.query_id                  # Trae el Id del registro según Nombre o DNI.
connection = App_Odonto_SQL.connection            # Parámetros de conexión a la base de datos.
execute_query = App_Odonto_SQL.execute_query      # Función para ejecutar alguna consulta SQL.
query_nombre_dni=App_Odonto_SQL.query_nombre_dni    # Trae el nombre del paciente según el Id consultado.
query_dni_nombre=App_Odonto_SQL.query_dni_nombre    # Trae el DNI del paciente según el Id consultado.
crear_presupuesto= App_Odonto_SQL.crear_presupuesto    # Carga datos en la tabla de presupuestos.

"""Está 'rota' la búsqueda (App_Odonto_Consulta_DB) por DNI y por nombre porque iba a hacerla por número de orden"""

#-----------------------------Creación de la GUI-------------------------------------------------------------------------

#-------Carga de presupuestos
formatos={'Letra':'Italic','Tamaño título':14,'Tamaño bloques':12}

presupuestos_col= [
                [sg.Text('Buscar por N° de Orden',size=(20,1),font=(formatos['Letra'],formatos['Tamaño título']))], #Consultar DNI del paciente para cargarle un presupuesto.
                [sg.Combo(values=(query_pacientes_dni()),default_value='Seleccionar',size=(15,1),font=(formatos['Letra'][0],11),enable_events=True,key='-ORDEN-')],
                #[sg.Text('Buscar por D.N.I',size=(20,1),font=(formatos['Letra'],formatos['Tamaño título']))], #Consultar DNI del paciente para cargarle un presupuesto.
                #[sg.Combo(values=(query_pacientes_dni()),default_value='Seleccionar',size=(15,1),font=(formatos['Letra'][0],11),enable_events=True,key='-Lista DNI-')], 
                #[sg.Text('Buscar por Nombre',size=(20,1),font=(formatos['Letra'],formatos['Tamaño título']))], # Consultar nombre del paciente para cargarle un presupuesto.
                #[sg.Combo(values=(query_pacientes_nombre()),default_value='Seleccionar',size=(15,1),font=(formatos['Letra'][0],11),enable_events=True,key='-Lista NOM-')],  
                [sg.Text('DNI', size=(15,1),font=(formatos['Letra'],formatos['Tamaño bloques'])), sg.InputText(size=(30),key='-DNI-')],
                [sg.Text('Nombre', size=(15,1),font=(formatos['Letra'],formatos['Tamaño bloques'])), sg.InputText(size=(30),key='-Nombre-')],
                [sg.Text('Fecha', size=(15,1),font=(formatos['Letra'],formatos['Tamaño bloques'])), sg.InputText(size=(15),key='-Fecha-')],
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

window_presupuestos = sg.Window('Odonto Presupuestos', layout=layout_carga_presupuesto) 

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

        #nombre_prolijo=(values['-Lista NOM-']) # Venía entre llaves.
        #nombre=f'"{nombre_prolijo}"' 

        #new_dni = query_dni_nombre(dni_unico) # Le pasa el valor del nombre a la función para que traiga el DNI.    
        
        nombre_dni= query_nombre_dni(dni_unico) # Le pasa el valor del DNI a la función para que traiga el nombre. 
        
        # Actualización de los valores en los cuadros y listas.
        
        window_presupuestos['-Nombre-'].update(nombre_dni[0])
        window_presupuestos['-Lista DNI-'].update(dni_unico)    
        window_presupuestos['-Lista NOM-'].update(nombre_dni[0])

    if event == '-Lista NOM-':
        nombre_prolijo=(values['-Lista NOM-']) # Venía entre llaves.
        nombre=f'"{nombre_prolijo}"'   # Limpia el texto para pasarlo a la función.
        
        dni_nombre=query_dni_nombre(nombre)  # Trae el DNI del paciente según el Id relacionado con el Nombre.

        # Actualización de los valores en los cuadros y listas.
        window_presupuestos['-Nombre-'].update(nombre_prolijo) 
        window_presupuestos['-DNI-'].update(dni_nombre[0])
        window_presupuestos['-Lista DNI-'].update(dni_nombre[0])
        window_presupuestos['-Lista NOM-'].update(nombre_prolijo)

    if event == 'Cargar':
        #(-------Carga en BD-------)
        new_record = execute_query(connection, crear_presupuesto(values['-DNI-'],values['-Nombre-'],values['-TRA-'],values['-Fecha-'],values['-PRECIO-'],values['-PAGO-'],
        values['-CUOTAS-'])) # Escribe datos nuevos.    
        sg.popup('Datos guardados!')
        clear_input()
        window_presupuestos['-Lista DNI-'].update('Seleccionar')
        window_presupuestos['-Lista NOM-'].update('Seleccionar')
    if event == 'Limpiar':
        clear_input()
        window_presupuestos['-Lista DNI-'].update('Seleccionar')
        window_presupuestos['-Lista NOM-'].update('Seleccionar')
window_presupuestos.close()

