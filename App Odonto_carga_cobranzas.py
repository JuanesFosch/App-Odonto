# Código que genera una GUI para ingresar datos de presupuesto en una base de datos y en un archivo de Excel existentes.

import PySimpleGUI as sg
import App_Lolo_SQL

connection = App_Lolo_SQL.connection            # Parámetros de conexión a la base de datos.
execute_query = App_Lolo_SQL.execute_query      # Función para ejecutar alguna consulta SQL.

query_pacientes_dni= App_Lolo_SQL.query_pacientes_dni           # Trae los DNI de los pacientes.
query_pacientes_nombre= App_Lolo_SQL.query_pacientes_nombre     # Trae los Nombres de los pacientes.
query_id=App_Lolo_SQL.query_id                  # Trae el Id del registro según Nombre o DNI de la tabla 'pacientes'.

query_nombre_id=App_Lolo_SQL.query_nombre_id    # Trae el nombre del paciente según el Id consultado.
query_dni_id=App_Lolo_SQL.query_dni_id    # Trae el DNI del paciente según el Id consultado.

query_tratamiento= App_Lolo_SQL.query_tratamiento   # Trae el tratamiento del paciente según el Id consultado.
query_presupuesto= App_Lolo_SQL.query_presupuesto       # Trae el presupuesto del paciente según el Id consultado.
query_id_cobranzas= App_Lolo_SQL.query_id_cobranzas    # Trae el Id del registro según Nombre o DNI de la tabla 'cobranzas'.
query_deuda = App_Lolo_SQL.query_deuda              # Trae la deuda del paciente según el Id consultado.

crear_cobro= App_Lolo_SQL.crear_cobro    # Carga datos en la tabla 'cobranzas'.

#-----------------------------Creación de la GUI-------------------------------------------------------------------------

#-------Carga de cobros
formatos={'Letra':'Italic','Tamaño título':14,'Tamaño bloques':12}

cobros_col= [
                [sg.Text('Buscar por D.N.I',size=(20,1),font=(formatos['Letra'],formatos['Tamaño título']))], #Consultar DNI del paciente para cargarle un presupuesto.
                [sg.Combo(values=(query_pacientes_dni()),default_value='Seleccionar',size=(15,1),font=(formatos['Letra'][0],11),enable_events=True,key='-Lista DNI-')], 
                [sg.Text('Buscar por Nombre',size=(20,1),font=(formatos['Letra'],formatos['Tamaño título']))], # Consultar nombre del paciente para cargarle un presupuesto.
                [sg.Combo(values=(query_pacientes_nombre()),default_value='Seleccionar',size=(15,1),font=(formatos['Letra'][0],11),enable_events=True,key='-Lista NOM-')],  
                [sg.Text('DNI', size=(15,1),font=(formatos['Letra'],formatos['Tamaño bloques'])), sg.InputText(size=(30),key='-DNI-')],
                [sg.Text('Nombre', size=(15,1),font=(formatos['Letra'],formatos['Tamaño bloques'])), sg.InputText(size=(30),key='-Nombre-')],
                [sg.Text('Fecha', size=(15,1),font=(formatos['Letra'],formatos['Tamaño bloques'])), sg.InputText(size=(15),key='-Fecha-')],
                [sg.Text('Tratamiento', size=(15,1),font=(formatos['Letra'],formatos['Tamaño bloques'])), sg.InputText(size=(30),key='-TRA-')],
                [sg.Text('Presupuestado', size=(15,1),font=(formatos['Letra'],formatos['Tamaño bloques'])), sg.InputText(size=(10),key='-PRECIO-')],
                [sg.Text('Deuda', size=(15,1),font=(formatos['Letra'],formatos['Tamaño bloques'])), sg.InputText(size=(10),key='-DEUDA-')],
                [sg.Text('Cuánto pagó', size=(15,1),font=(formatos['Letra'],formatos['Tamaño bloques'])), sg.InputText(size=(10),key='-COBRO-')],
                [sg.Text('Forma de pago', size=(15,1),font=(formatos['Letra'],formatos['Tamaño bloques'])), sg.InputText(size=(10),key='-PAGO-')]
                ]



layout_carga_cobros = [
    [sg.Text('Cargar cobro a:',font=(formatos['Letra'],formatos['Tamaño título']))],
    [sg.Column(cobros_col,element_justification='l',vertical_alignment='t',grab=True)],
    [sg.Submit('Cargar'), sg.Button('Limpiar'), sg.Exit('Salir',key='-SALIR-')]
    ]

window_cobros = sg.Window('Odonto Cobranzas', layout=layout_carga_cobros) 

#------------------------------------Bucle de eventos---------------------------------------------------------------
def clear_input():
    for key in values:
        window_cobros[key]('') #Pone una string vacía en el lugar donde había otra. Identifica el lugar por la 'key'.
    return None

while True:
    event, values = window_cobros.read() # Toma los 'event' y 'values' de la 'window' (según los parámetros de la función "read()"). En este caso son los event y values del 'layout' creado.
    dni_pac=query_pacientes_dni() # Trae los DNI de los pacientes.
    nombre_pacientes= query_pacientes_nombre() # Trae los Nombres de los pacientes.
    #nombre_por_id= query_nombre() #Trae los nombres de los pacientes según el Id.

    window_cobros['-Lista NOM-'].update(values=nombre_pacientes)
    window_cobros['-Lista DNI-'].update(values=dni_pac)

    if event == sg.WIN_CLOSED or event == '-SALIR-':
        break
    if event == '-Lista DNI-':
        dni_unico=(values['-Lista DNI-'])
        window_cobros['-DNI-'].update(dni_unico)

        id_dni = query_id(dni_unico) # Le pasa el valor del DNI a la función para que traiga el Id.
        id_cobranzas= query_id_cobranzas(dni_unico)

        nombre_id= query_nombre_id(id_dni[0]) # Trae el nombre del paciente según el Id relacionado con el DNI.
        #print(nombre_id[0])
        tratamiento= query_tratamiento(id_dni[0])
        presupuesto = query_presupuesto(id_dni[0])
        deuda= query_deuda(id_cobranzas[0])
        
        # Actualización de los valores en los cuadros y listas.
        window_cobros['-Nombre-'].update(nombre_id[0])
        window_cobros['-Lista DNI-'].update(dni_unico)    
        window_cobros['-Lista NOM-'].update(nombre_id[0])
        window_cobros['-TRA-'].update(tratamiento[0])
        window_cobros['-PRECIO-'].update(presupuesto[0])
        window_cobros['-DEUDA-'].update(deuda[0])

    if event == '-Lista NOM-':
        nombre_prolijo=(values['-Lista NOM-']) # Venía entre llaves.
        nombre=f'"{nombre_prolijo}"'   # Limpia el texto para pasarlo a la función.
        
        id_nombre= query_id(nombre)  # Le pasa el valor del Nombre a la función para que traiga el Id.
        id_cobranzas= query_id_cobranzas(nombre)

        dni_id=query_dni_id(id_nombre[0])  # Trae el DNI del paciente según el Id relacionado con el Nombre.
        tratamiento= query_tratamiento(id_nombre[0])
        presupuesto = query_presupuesto(id_nombre[0])
        deuda= query_deuda(id_cobranzas[0])
        
        # Actualización de los valores en los cuadros y listas.
        window_cobros['-Nombre-'].update(nombre_prolijo) 
        window_cobros['-DNI-'].update(dni_id[0])
        window_cobros['-Lista DNI-'].update(dni_id[0])
        window_cobros['-Lista NOM-'].update(nombre_prolijo)
        window_cobros['-TRA-'].update(tratamiento[0])
        window_cobros['-PRECIO-'].update(presupuesto[0])
        window_cobros['-DEUDA-'].update(deuda[0])

    if event == 'Cargar':
        #(-------Carga en BD-------)
        new_record = execute_query(connection, crear_cobro(values['-DNI-'],values['-Nombre-'],values['-Fecha-'],values['-TRA-'],values['-PRECIO-'],
        values['-COBRO-'],values['-PAGO-'])) # Escribe datos nuevos.    
        sg.popup('Datos guardados!')
        clear_input()
        window_cobros['-Lista DNI-'].update('Seleccionar')
        window_cobros['-Lista NOM-'].update('Seleccionar')
    if event == 'Limpiar':
        clear_input()
        window_cobros['-Lista DNI-'].update('Seleccionar')
        window_cobros['-Lista NOM-'].update('Seleccionar')
window_cobros.close()

