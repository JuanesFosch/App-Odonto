import PySimpleGUI as sg
#import App_Lolo_SQL

#connection = App_Lolo_SQL.connection
#create_users = App_Lolo_SQL.create_users
#execute_query = App_Lolo_SQL.execute_query

#-----------------------------Creación de la GUI-------------------------------------------------------------------------



#-------Consulta de pacientes
formatos={'Letra':'Italic','Tamaño título':14,'Tamaño bloques':12}

col_izquierda=[
                [sg.Combo(values=('Paciente 1','Paciente 2','Paciente 3'),default_value='Paciente 1',enable_events=True,key='-PAC-')],
                [sg.Text('Info contacto', size=(10,1),font=(formatos['Letra'],formatos['Tamaño título']))],
                [sg.Text('Nombre, Mail, DNI', size=(15,1),font=(formatos['Letra'],formatos['Tamaño bloques']))],
                [sg.Text('Historia Clínica', size=(15,1),font=(formatos['Letra'],formatos['Tamaño bloques']))],
                [sg.Multiline(pad=(5,1),size=(30,5),key='-Historia-')], 
                [sg.Text('+ Notas', size=(10,1),font=(formatos['Letra'],formatos['Tamaño bloques']))]
            ]

col_derecha=[
            [sg.Text('Deuda', size=(15,1),font=(formatos['Letra'],formatos['Tamaño bloques']))],
            [sg.Text('   ', size=(15,1),background_color='white',font=(formatos['Letra'],formatos['Tamaño bloques']))],
            [sg.Text('Costo: '+formatos['Letra'],background_color='black', size=(15,1),font=(formatos['Letra'],formatos['Tamaño bloques']))],
            [sg.Text('Valor Presupuesto', size=(15,1),font=(formatos['Letra'],formatos['Tamaño bloques']))],
            [sg.Text('Forma de Pago', size=(15,1),font=(formatos['Letra'],formatos['Tamaño bloques']))]
            ]

layout_consulta_pacientes=[
                            [sg.Column(col_izquierda,element_justification='l',vertical_alignment='t',grab=True), 
                            sg.VerticalSeparator(),
                            sg.Column(col_derecha,element_justification='l',vertical_alignment='t',grab=True)]
                            ]

window_consulta_pacientes = sg.Window('Odonto', layout=layout_consulta_pacientes)

#------------------------------------Bucle de eventos---------------------------------------------------------------
window_consulta_pacientes.read()

""" Queda actualizar los elementos de texto para que puedan tener los datos a mostrar.
    Queda declarar los Eventos y los Values. En este caso el único evento es la selección de un paciente, y los valores
    son los valores de cada columna de la tabla en la DB. Se buscan estos valores para ponerlos en el elemento correspondiente."""

"""while True:
    event, values = window_consulta_pacientes.read() # Toma los 'event' y 'values' de la 'window' (según los parámetros de la función "read()"). En este caso son los event y values del 'layout' creado.
    if event == sg.WIN_CLOSED or event == 'Exit':
        break"""
    
