import PySimpleGUI as sg
import App_Lolo_SQL

connection = App_Lolo_SQL.connection
query_users = App_Lolo_SQL.query_users
query_pacientes= App_Lolo_SQL.query_pacientes
query_costo=App_Lolo_SQL.query_costo
execute_query = App_Lolo_SQL.execute_query

#-----------------------------Creación de la GUI-------------------------------------------------------------------------



#-------Consulta de pacientes
formatos={'Letra':'Italic','Tamaño título':14,'Tamaño bloques':12}

col_izquierda=[
                [sg.Combo(values=('Paciente 1','Paciente 2','Paciente 3'),default_value='Nombre',enable_events=True,key='-PAC-')],
                [sg.Button('Consulta',enable_events=True,key='-CONSULTA-')],
                [sg.Text('Info contacto', size=(10,1),font=(formatos['Letra'],formatos['Tamaño título']),enable_events=True,key='-TEXT-')],
                [sg.Text('Nombre' +' - '+ 'Mail' +' - '+ 'DNI', size=(15,1),font=(formatos['Letra'],formatos['Tamaño bloques']),key='-INFO-')],
                [sg.Text('Historia Clínica', size=(15,1),font=(formatos['Letra'],formatos['Tamaño bloques']))],
                [sg.Multiline(default_text='Texto',pad=(5,1),size=(30,5),key='-Historia-')], 
                [sg.Text('+ Notas', size=(10,1),font=(formatos['Letra'],formatos['Tamaño bloques']))]
            ]

col_derecha=[
            [sg.Text('Deuda', size=(15,1),font=(formatos['Letra'],formatos['Tamaño bloques']))],
            [sg.Text('   ', size=(15,1),background_color='white',font=(formatos['Letra'],formatos['Tamaño bloques']))],
            [sg.Text('Costo: '+formatos['Letra'],background_color='black', size=(15,1),font=(formatos['Letra'],formatos['Tamaño bloques']),key='-COSTO-')],
            [sg.Text('Valor Presupuesto', size=(15,1),font=(formatos['Letra'],formatos['Tamaño bloques']))],
            [sg.Text('Forma de Pago', size=(15,1),font=(formatos['Letra'],formatos['Tamaño bloques']))]
            ]

layout_consulta_pacientes=[
                            [sg.Column(col_izquierda,element_justification='l',vertical_alignment='t',grab=True), 
                            sg.VerticalSeparator(),
                            sg.Column(col_derecha,element_justification='l',vertical_alignment='t',grab=True)],
                            [sg.Exit('Salir',key='-SALIR-')]
                            ]

window_consulta_pacientes = sg.Window('Odonto', layout=layout_consulta_pacientes)

#------------------------------------Bucle de eventos---------------------------------------------------------------


while True:
    event, values = window_consulta_pacientes.read() # Toma los 'event' y 'values' de la 'window' (según los parámetros de la función "read()"). En este caso son los event y values del 'layout' creado.
    if event == sg.WIN_CLOSED or event == '-SALIR-':
        break
    if event == '-CONSULTA-':
        
        dni_pac=query_pacientes('-CONSULTA-') # Trae los DNI de los pacientes.
   
        window_consulta_pacientes['-PAC-'].update(values=dni_pac) # Modifica los valores de la lista desplegable, reemplazándolos con los DNI.
       
        window_consulta_pacientes['-PAC-'].update('DNI')


    if event == '-PAC-':
        #a=''.join((values['-PAC-'])) # Toma el valor de la tupla que devuelve activar la lista desplegable, y lo transforma en string. Sirve para consultar con nombres.
        
        pacientes=(values['-PAC-']) # Toma los valores de la lista desplegable modificada, osea los DNI.
        info=query_users('-PAC-',pacientes) # Activa la consulta de datos, entregando a la función el evento donde se activa la lista desplegable, y el valor que es un DNI de esa lista.
        costo=query_costo('-PAC-',pacientes)
        #window_consulta_pacientes['-INFO-'].update(a)
        window_consulta_pacientes['-INFO-'].update(info) # Modifica el texto debajo de 'Info Contacto' con la información traída desde la consulta
        window_consulta_pacientes['-COSTO-'].update(costo)
window_consulta_pacientes.close()       



""" Queda actualizar los elementos de texto para que puedan tener los datos a mostrar.
    Queda declarar los Eventos y los Values. En este caso el único evento es la selección de un paciente, y los valores
    son los valores de cada columna de la tabla en la DB. Se buscan estos valores para ponerlos en el elemento correspondiente (con VALUES %s?)."""

    
