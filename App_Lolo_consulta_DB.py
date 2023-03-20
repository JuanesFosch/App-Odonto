import PySimpleGUI as sg
import App_Lolo_SQL

connection = App_Lolo_SQL.connection
query_info = App_Lolo_SQL.query_info # Trae el nombre, teléfono y mail de los pacientes.
query_pacientes_dni= App_Lolo_SQL.query_pacientes_dni # Trae los DNI de los pacientes.
query_pacientes_nombre= App_Lolo_SQL.query_pacientes_nombre # Trae los Nombres de los pacientes.
query_historia= App_Lolo_SQL.query_historia # Trae la hsitoria clínica de los pacientes.
query_costo=App_Lolo_SQL.query_costo # Trae el costo de los pacientes.
query_presupuesto = App_Lolo_SQL.query_presupuesto # Trae el presupuesto de los pacientes.
query_forma_de_pago= App_Lolo_SQL.query_forma_de_pago # Trae la forma de pago de los pacientes.


#-----------------------------Creación de la GUI-------------------------------------------------------------------------



#-------Consulta de pacientes
formatos={'Letra':('Helvetica','bold','black'),'Tamaño título':14,'Tamaño bloques':12}

col_izquierda=[
                [sg.Text('Consultar por D.N.I',size=(10,1),font=(formatos['Letra'],formatos['Tamaño título']))],[sg.Text('Consultar por Nombre',size=(10,1),font=(formatos['Letra'],formatos['Tamaño título']))],
                [sg.Combo(values=(query_pacientes_dni()),default_value='Seleccionar',enable_events=True,key='-PAC-')], 
                [sg.Combo(values=(query_pacientes_nombre()),default_value='Seleccionar',enable_events=True,key='-NOM-',size=(15,1))],
                [sg.Text('Info contacto', size=(10,1),font=(formatos['Letra'],formatos['Tamaño título']),enable_events=True,key='-TEXT-')],
                [sg.Text('Nombre' +' - '+ 'Mail' +' - '+ 'DNI', size=(25,1),font=(formatos['Letra'][0],formatos['Tamaño bloques'],formatos['Letra'][1]),key='-INFO-')],
                [sg.Text('Historia Clínica', size=(15,1),font=(formatos['Letra'],formatos['Tamaño bloques']))],
                [sg.Multiline(default_text='Texto',pad=(5,1),size=(30,5),key='-Historia-')], 
                [sg.Text('+ Notas', size=(10,1),font=(formatos['Letra'],formatos['Tamaño bloques']))]
            ]

col_derecha=[
            [sg.Text('Deuda', size=(15,1),font=(formatos['Letra'],formatos['Tamaño bloques']))],
            [sg.Text('   ', size=(15,1),background_color='white',text_color='black',font=(formatos['Letra'],formatos['Tamaño bloques']))],
            [sg.Text('Costo: ', size=(15,1),font=(formatos['Letra'],formatos['Tamaño bloques']))],
            [sg.Text('   ', size=(15,1),background_color='white',text_color='black',font=(formatos['Letra'],formatos['Tamaño bloques']),key='-COSTO-')],
            [sg.Text('Valor Presupuesto', size=(15,1),font=(formatos['Letra'],formatos['Tamaño bloques']))],
            [sg.Text('   ', size=(15,1),background_color='white',text_color='black',font=(formatos['Letra'],formatos['Tamaño bloques']),key='-PREP-')],
            [sg.Text('Forma de Pago', size=(15,1),font=(formatos['Letra'],formatos['Tamaño bloques']))],
            [sg.Text('   ', size=(15,1),background_color='white',text_color='black',font=(formatos['Letra'],formatos['Tamaño bloques']),key='-FORMA-')]
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
    dni_pac=query_pacientes_dni() # Trae los DNI de los pacientes.
    nombre_pacientes= query_pacientes_nombre() # Trae los Nombres de los pacientes.

    window_consulta_pacientes['-PAC-'].update(values=dni_pac) # Modifica los valores de la lista desplegable, reemplazándolos con los DNI.
    window_consulta_pacientes['-PAC-'].update('DNI')

    window_consulta_pacientes['-NOM-'].update(values=nombre_pacientes)
    window_consulta_pacientes['-NOM-'].update('Nombre')  
    
    if event == sg.WIN_CLOSED or event == '-SALIR-':
        break
    
    """if event == window_consulta_pacientes.read():
        
        dni_pac=query_pacientes() # Trae los DNI de los pacientes.
   
        window_consulta_pacientes['-PAC-'].update(values=dni_pac) # Modifica los valores de la lista desplegable, reemplazándolos con los DNI.
        window_consulta_pacientes['-PAC-'].update('DNI')       """

    if event == '-PAC-':
        #a=''.join((values['-PAC-'])) # Toma el valor de la tupla que devuelve activar la lista desplegable, y lo transforma en string. Sirve para consultar con nombres.
        
        limpiar=''
        pacientes_nombre=(values['-NOM-'])
        pacientes_dni=(values['-PAC-']) # Toma los valores de la lista desplegable modificada, osea los DNI.
        info=query_info('-PAC-',pacientes_dni) # Activa la consulta de datos, entregando a la función el evento donde se activa la lista desplegable, y el valor que es un DNI de esa lista.
        historia=query_historia('-PAC-',pacientes_dni)
        presupuesto=query_presupuesto('-PAC-',pacientes_dni)
        forma_de_pago=query_forma_de_pago('-PAC-',pacientes_dni)
        costo=query_costo('-PAC-',pacientes_dni)
 

        #window_consulta_pacientes['-INFO-'].update(a)
        #window_consulta_pacientes['-INFO-'].update(limpiar)
        window_consulta_pacientes['-PAC-'].update(pacientes_dni)
        #window_consulta_pacientes['-NOM-'].update(pacientes_nombre)
        window_consulta_pacientes['-INFO-'].update(info) # Modifica el texto debajo de 'Info Contacto' con la información traída desde la consulta
        window_consulta_pacientes['-Historia-'].update(historia)
        window_consulta_pacientes['-COSTO-'].update(costo)
        window_consulta_pacientes['-PREP-'].update(presupuesto)
        window_consulta_pacientes['-FORMA-'].update(forma_de_pago)

    if event == '-NOM-':
        #a=''.join((values['-PAC-'])) # Toma el valor de la tupla que devuelve activar la lista desplegable, y lo transforma en string. Sirve para consultar con nombres.
        
        pacientes_nombre=(values['-NOM-'])
        nombre=f'"{pacientes_nombre}"'
        info=query_info('-NOM-',nombre) # Activa la consulta de datos, entregando a la función el evento donde se activa la lista desplegable, y el valor que es un DNI de esa lista.
        window_consulta_pacientes['-INFO-'].update(info)

        historia=query_historia('-NOM-',nombre)
        presupuesto=query_presupuesto('-NOM-',nombre)
        forma_de_pago=query_forma_de_pago('-NOM-',nombre)
        costo=query_costo('-NOM-',nombre)
 # Probrar excepción de errores cuando no estén bien ingresados los datos.

        window_consulta_pacientes['-NOM-'].update(pacientes_nombre)
        window_consulta_pacientes['-INFO-'].update(info) # Modifica el texto debajo de 'Info Contacto' con la información traída desde la consulta
        window_consulta_pacientes['-Historia-'].update(historia)
        window_consulta_pacientes['-COSTO-'].update(costo)
        window_consulta_pacientes['-PREP-'].update(presupuesto)
        window_consulta_pacientes['-FORMA-'].update(forma_de_pago) 

    
window_consulta_pacientes.close()       



""" Queda actualizar los elementos de texto para que puedan tener los datos a mostrar.
    Queda declarar los Eventos y los Values. En este caso el único evento es la selección de un paciente, y los valores
    son los valores de cada columna de la tabla en la DB. Se buscan estos valores para ponerlos en el elemento correspondiente (con VALUES %s?)."""

    
