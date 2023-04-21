# Código que genera una GUI para ingresar datos de pacientes en una base de datos y en un archivo de Excel existentes.

import PySimpleGUI as sg
import App_Odonto_SQL

import pandas as pd



connection = App_Odonto_SQL.connection            # Crea la conexión a la base de datos.
crear_pacientes = App_Odonto_SQL.crear_pacientes          # Crea usuarios en la base de datos.
execute_query = App_Odonto_SQL.execute_query          # Ejecuta la query según un evento.
#consulta= App_Odonto_consulta_DB esto era para cambiar entre ventanas.

EXCEL_FILE =r'C:\Users\juanf\Desktop\Otras Apps\App Odonto\desktop_Odonto\Imágenes y otros\Odonto.xlsx'
df_pacientes=pd.read_excel(EXCEL_FILE,sheet_name='Hoja1')

#-----------------------------Creación de la GUI-------------------------------------------------------------------------

#-------Carga de pacientes
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
    [sg.Button('Ir a Consulta',enable_events=True,key='-CONS-',pad=(5,30))],
    [sg.Button('Ir a Carga de Presupuesto',enable_events=True,pad=(5,5))]
    ]

"""Cobro_col=[
    [sg.Text('Cobranza:', size=(10,1),font=(formatos['Letra'],formatos['Tamaño título']))],
    [sg.Text('Costo', size=(10,1),font=(formatos['Letra'],formatos['Tamaño bloques'])), sg.InputText(pad=(21,1),size=(15,1),key='-Costo-')], #Esto va en otra columna
    [sg.Text('Presupuesto', size=(10,1),font=(formatos['Letra'],formatos['Tamaño bloques'])), sg.InputText(pad=(21,1),size=(15,1),key='-Presupuesto-')], #Esto va en otra columna
    [sg.Text('Forma de Pago', size=(12,1),font=(formatos['Letra'],formatos['Tamaño bloques'])), sg.InputText(pad=(1,1),size=(15,1),key='-Pago-')],
    [sg.Text('Notas', size=(5,1),font=(formatos['Letra'],formatos['Tamaño bloques'])), sg.Multiline(pad=(70.5,1),size=(30,5),key='-Notas-')] #Esto va en otra columna
    ]"""

layout_pacientes = [
    [sg.Text('Carga de pacientes:',font=(formatos['Letra'],formatos['Tamaño título']))],
    [sg.Column(pacientes_col,element_justification='l',vertical_alignment='t',grab=True), 
    sg.VerticalSeparator(),
    sg.Column(OS_Prepaga_col,element_justification='l',vertical_alignment='t',grab=True),
    sg.VerticalSeparator()],
    #sg.Column(Cobro_col,element_justification='l',vertical_alignment='t',grab=True)],
    [sg.Submit('Cargar'), sg.Button('Limpiar'), sg.Exit('Salir',key='-SALIR-')]
    ]

window_pacientes = sg.Window('Odonto Carga de Pacientes', layout=layout_pacientes) 


#------------------------------------Bucle de eventos---------------------------------------------------------------

"""El código para consultar debería ser un SELECT de la DB y que reemplace o haga un update al Texto de un ELEMENTO.
   Después del SELECT, un WHERE para cada nombre de campo o columna (o revisar fotos requerimientos).
   Revisar en internet como hacer ese filtro de WHERE, podría ser similar al 'VALUES %s'.
   Podría ser en otro módulo."""

def clear_input():
    for key in values:
        window_pacientes[key]('') #Pone una string vacía en el lugar donde había otra. Identifica el lugar por la 'key'.
    return None

while True:
    event, values = window_pacientes.read() # Toma los 'event' y 'values' de la 'window' (según los parámetros de la función "read()"). En este caso son los event y values del 'layout' creado.
    if event == sg.WIN_CLOSED or event == '-SALIR-':
        break
    if event == 'Limpiar':
        clear_input()
    if event == 'Cargar':
        #(-------Carga en BD-------)
        new_record = execute_query(connection, crear_pacientes(values['-Nombre-'],values['-DNI-'],values['-Tel-'],values['-Mail-'],values['-Historia-'],
        values['-Obra Social/Prepaga-'],values['-Código-'])) # Escribe datos nuevos.
        #(-------Carga en Excel-------)
        new_record_excel = pd.DataFrame(values, index=[0])
        df = pd.concat([df_pacientes, new_record_excel], ignore_index=True) # Escribe datos nuevos.
        #update = pd.DataFrame.update(self= df,other=new_record,overwrite=True) # Sobreescribe datos. Tiene que haber datos en las celdas para que funcione.
        with pd.ExcelWriter(EXCEL_FILE,mode='a',if_sheet_exists='overlay') as writer: # Función para escribir sobre una pestaña seleccionada y que no reemplace lo anterior.
            df.to_excel(writer,sheet_name='Hoja1', index=False)

        sg.popup('Datos guardados!')
        clear_input()
        #if event == '-CONS-':
           #import App_Odonto_consulta_DB
window_pacientes.close()