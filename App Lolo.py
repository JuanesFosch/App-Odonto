# Código que genera una GUI para ingresar datos en un archivo de Excel EXISTENTE.

import PySimpleGUI as sg
import pandas as pd


EXCEL_FILE =r'C:\Users\juanf\Desktop\Otras Apps\App Lolo\Odonto.xlsx'
df=pd.read_excel(EXCEL_FILE)

#print(df.info())



layout = [
    [sg.Text('Campos a llenar:')],
    [sg.Text('Nombre', size=(15,1)), sg.InputText(key='Nombre')],
    [sg.Text('DNI', size=(15,1)), sg.InputText(key='DNI')],
    [sg.Text('Obra Social/Prepaga', size=(15,1)), sg.InputText(key='Obra Social/Prepaga')],
    [sg.Submit(), sg.Button('Limpiar'), sg.Exit()]
]

window = sg.Window('Odonto', layout)

def clear_input():
    for key in values:
        window[key]('') #Pone una string vacía en el lugar donde había otra. Identifica el lugar por la 'key'.
    return None

while True:
    event, values = window.read() # Toma los 'event' y 'values' de la 'window' (según los parámetro de la función). En este caso son los event y values del 'layout' creado.
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Limpiar':
        clear_input()
    if event == 'Submit':
        new_record = pd.DataFrame(values, index=[0])
        df = pd.concat([df, new_record], ignore_index=True) # Escribe datos nuevos.
        #update = pd.DataFrame.update(self= df,other=new_record,overwrite=True) # Sobreescribe datos. Tiene que haber datos en las celdas para que funcione.
        df.to_excel(EXCEL_FILE, index=False)
        sg.popup('Datos guardados!')
        clear_input()
window.close()