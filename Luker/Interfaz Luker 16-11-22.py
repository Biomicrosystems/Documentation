# -*- coding: utf-8 -*-
"""
Created on Wed Nov  9 16:18:54 2022
@author: Santiago Tovar-Gabriel Mejia
"""

import PySimpleGUI as sg
import os
from PIL import Image
import datetime
import serial
import time
import json
from pathlib import Path

serial_path = '/dev/ttyUSB0'
serial_speed = 9600

# Test code uncomment the next line to get real function
arduino1 = serial.Serial()

# arduino1 = serial.Serial(serial_path, serial_speed)
# arduino2 = serial.Serial('/dev/ttyUSB0', 9600)

global rutaglobal, start_date, end_date, fermenter, plot, resampling

start_date = -1
end_date = -1
fermenter = -1
plot = 'complete_fermenter'
resampling = '12h'

sg.set_options(font=("Helvetica", 5), text_justification='center')
dias = 0
contdia = 0
instanteInicial = time.time()
print("Starting!")
contador = 0
rutaglobal = os.getcwd()  # "/home/pi/Raspduino"
# Set short name for Helvetica
hv = 'Helvetica'
os.getcwd()
w, h = sg.Window.get_screen_size()

fixed_height = 200
image = Image.open(os.path.abspath(
    os.path.join('resources', 'Proyect_Logo.png')))
height_percent = (fixed_height / float(image.size[1]))
width_size = int((float(image.size[0]) * float(height_percent)))
image = image.resize((width_size, fixed_height))
image.save('resources/Logos_documentación1.png')

settings_file = 'settings.json'
settings = {'-Image-': None}
if Path(settings_file).is_file():
    with open(settings_file, 'rt') as f:
        settings = json.load(f)
fixed_width1 = w-100
image1 = Image.open(os.path.abspath(
    os.path.join('resources', 'f1.jpeg')))
width_percent1 = (fixed_width1 / float(image1.size[0]))
height_size1 = int((float(image1.size[1]) * float(width_percent1)))
image1 = image1.resize((fixed_width1, height_size1))
image1.save('resources/probe1.png')
ferlist = ['Fermentador 1', 'Fermentador 2', 'Fermentador 3', 'Fermentador 4']

sg.theme('LightBrown11')
e = datetime.datetime.now()
global datei
datei = datetime.datetime.now()

col1 = [[sg.Text(' ' * 25,  size=(
    25, 1), font=(hv, 9)), sg.Text('Fermentación del Cacao',  size=(
        22, 1), font=(hv, 30)), sg.Text('2.0',  size=(
            3, 1), font=(hv, 9)), sg.Text(' ' * 15,  size=(
                15, 1), font=(hv, 9)), sg.Button('About us', key='about',
                                                 size=(9, 1), font=(
                                                     hv, 8)), sg.Exit(size=(5, 1), font=(
                                                         hv, 7))], [sg.Text('═' * 125, font=(hv, 8))],
    [sg.Text(' ' * 10, size=(
        10, 1), font=(hv, 9)), sg.Text('       ', key='lectura',  size=(10, 1), font=(hv, 10)), sg.Text('', size=(10, 1)), sg.Button('Iniciar', button_color='white on green', key='inicio', size=(10, 1), font=(
            hv, 9)),  sg.Text('Día #', key='dia', size=(20, 1), font=(hv, 25)), sg.Button('Finalizar', button_color='white on red', key='fin', size=(10, 1), font=(hv, 9))], [sg.Text('═' * 125, font=(hv, 8))],
    [sg.Text("Fecha de inicio:   %s/%s/%s" % (e.day, e.month, e.year),  size=(25, 1), font=(hv, 10)), sg.Text(' ' * 3, size=(
        3, 1)),
     sg.Text('Fecha final estimada:',  size=(16, 1), font=(hv, 10)), sg.Text('Elija una ->',
                                                                             key='-FINAL-', size=(12, 1), font=(hv, 10)),
     sg.CalendarButton("Fecha final", close_when_date_chosen=True, format='%d/%m/%Y',
                       target='-FINAL-',  font=(hv, 10), no_titlebar=False), sg.Text(' ' * 14, size=(
                           14, 1)),
     sg.Text('Número de Fermentadores detectados: ',  size=(32, 1), font=(hv, 10)), sg.Text('1',  key='nfer', size=(2, 1), font=(hv, 10))],
    [sg.Text('═' * 125, font=(hv, 8))],
    [sg.Text('Nombre encargado:',  size=(16, 1), font=(hv, 10)), sg.Input(
        default_text='Ingrese su nombre', key='encargado', size=(26, 1), font=(hv, 10)), sg.Text(' ' * 1,  size=(
            1, 1)), sg.Text('Ubicación:',  size=(10, 1), font=(hv, 10)), sg.Input(
        default_text='Ingrese su ubicación', key='ubicacion', size=(26, 1), font=(hv, 10)), sg.Text(' ' * 8,  size=(
            8, 1)), sg.Text('Tamaño',  size=(6, 1), font=(hv, 10)),  sg.InputCombo(('Grande', 'Pequeño'), size=(10, 2), font=(hv, 10), key='tamaño', default_value='Grande')]]

col2 = [[sg.Text('Panel de opciones gráficas', font=(hv, 15))],
        [sg.Text('Tipo de Gráfica:', font=(hv, 12))],
        [sg.InputCombo(('Gráficas completas', 'Violin plot', 'Sensores por fermentador',
                        'Promedio y desviación estándar', 'Perfil 3D', 'Cámara termica'),
                       size=(40, 10), font=(hv, 13), key='graphtype', default_value='Gráficas completas')],
        [sg.Text('Fermentador a graficar:', font=(hv, 12))],
        [sg.InputCombo(ferlist,
                       size=(40, 10), font=(hv, 13), key='combofer', default_value='Fermentador 1'),

         sg.Button('Graficar', key='buttongraficar',
                   size=(13, 1), font=(hv, 13))],
        [sg.Checkbox('Resampling', key='checkresamp',
                     size=(50, 1), default=False, font=(hv, 11))],
        [sg.InputCombo(('1 h', '2 h',
                        '3 h', '6 h', '12 h', '1D'), size=(40, 10), font=(hv, 11),
                       key='hourcombo', default_value='12 hr')],
        [sg.Checkbox('Elegir rango de fechas', key='checkDate',
                     size=(50, 1), default=False, font=(hv, 11))],
        [sg.Text('Fecha inicial gráfica:',  size=(22, 1), font=(hv, 10), key='InicialText'),
         sg.Input('Elija una ->', key='-INICIALG-',
                  size=(12, 1), font=(hv, 10)),
        sg.CalendarButton("Fecha inicial", close_when_date_chosen=True, format='%d/%m/%Y',
                          target='-INICIALG-', key='InicialButton',  font=(hv, 10), no_titlebar=False), sg.Text(' ' * 14, size=(
                              14, 1))],
        [sg.Text('Fecha final gráfica:',  size=(22, 1), font=(hv, 10), key='FinalText'), sg.Input('Elija una ->',
                                                                                                  key='-FINALG-', size=(12, 1), font=(hv, 10)),
         sg.CalendarButton("Fecha final", close_when_date_chosen=True, format='%d/%m/%Y',
                           target='-FINALG-', key='FinalButton',  font=(hv, 10), no_titlebar=False), sg.Text(' ' * 14, size=(
                               15, 1))],
        [sg.Button('Mostrar desempeño semanal',
                   key='buttondesempeño', size=(30, 1), font=(hv, 13))],
        [sg.Text('═' * 80, font=(hv, 8))]]
col3 = [[sg.Text('Registro de eventos', font=(hv, 15)), sg.Text('', font=(hv, 11), size=(30, 1)), sg.Button('Guardar Evento', button_color='white on black',
                                                                                                            key='buttonnota', size=(20, 1), font=(hv, 10))],
        [sg.Multiline(default_text='Escribir apuntes del proceso',
                      key='multiline', size=(80, 4), font=("Helvetica", 11))],
        [sg.Button('Registrar Volteo',
                   key='volteo', size=(63, 1), font=(hv, 13))],
        [sg.Text('═' * 83, font=(hv, 8))],

        [sg.Text('Ubicación de datos', font=(hv, 15))],
        [sg.Input(default_text='rutaglobal', key='fileinput', size=(60, 1), font=(
            hv, 11)), sg.Text('', size=(2, 1)), sg.Button('Cambiar Ubicación', key='buttonfile', size=(15, 1), font=(hv, 11))],
        [sg.Text('═' * 83, font=(hv, 8))],
        [sg.Text(' ' * 80, font=(hv, 8))],
        [sg.Text(' ' * 80, font=(hv, 8))],
        [sg.Text(' ' * 80, font=(hv, 8))],
        [sg.Text(' ' * 80, font=(hv, 8))]

        ]

colprin = [
    [sg.Image(os.path.abspath(os.path.join('resources', 'Logos_documentación1.png')), size=(
        width_size, fixed_height)), sg.Column(col1)],
    [sg.Text('═' * 173, font=(hv, 8))],
    [sg.Text('Condiciones Ambientales', size=(36, 1), font=(hv, 23)),
     sg.Text('', size=(5, 1), font=(hv, 10)),
     sg.Text('Fermentadores', size=(34, 1), font=(hv, 23))],
    [sg.Text(' ' * 5,  size=(
        5, 1), font=(hv, 9)), sg.Text('  --  °C ',  key='Tamb', size=(6, 1), font=(hv, 40)),
     sg.Text(' ', size=(8, 1), font=(hv, 20)),
     sg.Text('  --  %', size=(6, 1), font=(hv, 40), key='Hamb'),
     sg.Text(' ', size=(9, 1), font=(hv, 40)),
     sg.Text(' --  °C', size=(6, 1), font=(hv, 40), key='Tfer')],
    [sg.Text('Temperatura', size=(28, 1), font=(hv, 14)),
        sg.Text('Humedad', size=(28, 1), font=(hv, 14)),
        sg.Text('', size=(17, 1), font=(hv, 8)),
        sg.Text('Temperatura Promedio', size=(38, 1), font=(hv, 14))],
    [sg.Text('═' * 173, font=(hv, 8))],
    [sg.Column(col2), sg.Column(col3)],

    #  [sg.Image(os.path.abspath(os.path.join('resources', 'probe1.png')),
    [sg.Image(filename=settings['-Image-'], visible=(settings['-Image-'] is not None),
              size=(fixed_width1, height_size1), key="ImagePlot")],
    [sg.Text(' ' * 173, font=(hv, 8))],
    [sg.Text('═' * 173, font=(hv, 8))]

]


layout = [[sg.Column(colprin, scrollable=True,
                     vertical_scroll_only=True, size_subsample_height=1)]]


window = sg.Window('Control Ambiental Fermentación', layout,
                   location=(0, 0), size=(w, h), resizable=True, finalize=True)
# window.Maximize()

var = False
arranque = False
act = False
aviso = 0
rutan = rutaglobal+"\\notas "+datei.strftime("%m-%d-%Y")+".txt"
outFile = open(rutan, "a")

while True:

    event, values = window.read(timeout=10)

    if event == 'inicio':
        outFile = open(rutan, "a")
        arranque = True
        contdia = datetime.datetime.now()  # - timedelta(days=7)

    if((var == False and contador > 0) and act == False):
        window.Element('lectura').Update('')
        act = True
    if (((((int(time.time()-instanteInicial))/60) > 1.1) or contador == 0) and arranque == True):
        # comando = raw_input('Introduce un comando: ') #Input
        # arduino.write(comando) #Mandar un comando hacia Arduino
        if(contador == 0):
            window.Element('lectura').Update('Sin datos')

        instanteInicial = time.time()
        dif = datetime.datetime.now()-contdia
        dias = dif.days
        window.Element('dia').Update('Día # ' + str(dias))
       # arduino1.write(str.encode("SIU"))
        contador = 1
        print("Escribiendo")

        var = True

    if ((((time.time()-instanteInicial)/60) > 0.9) and var == True):
        window.Element('lectura').Update('En lectura')
    if (((((time.time()-instanteInicial))/60) > 0.93) and var == True):
        print("Leyendo")

        var = False
        act = False
    if event == 'buttonnota':
        nota = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + \
            "  "+values['multiline']+"/n"
        outFile.write(nota)
        window.Element('multiline').Update('')
        sg.popup_timed(
            'Nota Guardada', 'Su nota fue almacenada en la ubicación elegida!', keep_on_top=True)
    if event == 'volteo':
        nota = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + \
            " Volteo/n"
        outFile.write(nota)
        sg.popup_timed(
            'Volteo Guardada', 'Su registro de volteo fue almacenada en la ubicación elegida!', keep_on_top=True)
    if event == 'buttonfile':
        folder = sg.popup_get_folder('Porfavor ingrese una nueva ubicación')
        if folder == 'OK':
            rutaglobal = folder
            window.Element('fileinput').Update(rutaglobal)
            rutan = rutaglobal+"'\\notas" + \
                datei.strftime("%m-%d-%Y")+".txt"
            outFile.close()
            outFile = open(rutan, "a")

    if dias > 14:
        aviso += 1

    if (aviso == 1) or (event in (sg.WIN_CLOSED, 'Exit', 'fin')):

        # Shows OK and Cancel buttons
        seg = sg.popup_ok_cancel(
            '¿Está seguro de finalizar la lectura de datos?', keep_on_top=True)
        if seg == 'OK':
            print('fin')
            window.Element('dia').Update('Día # ')
            window.Element('lectura').Update('')
            window.Element('Tamb').Update('  --  °C ')
            window.Element('Hamb').Update('  --  %')
            window.Element('Tfer').Update(' --  °C')
            outFile.close()
            arranque = False
            contador = 0
            var = False

            if event in (sg.WIN_CLOSED, 'Exit'):
                arduino1.close()  # Finalizamos la comunicacion
                break

    if (values['graphtype'] in ('Perfil 3D', 'Cámara termica')):
        window['checkDate'].update(disabled=True)
        window['checkDate'].update(visible=False)
        window['-INICIALG-'].update(visible=False)
        window['-FINALG-'].update(visible=False)
        window['InicialButton'].update(visible=False)
        window['InicialText'].update(visible=False)
        window['FinalButton'].update(visible=False)
        window['FinalText'].update(visible=False)
        start_date = -1
        end_date = -1

    if (values['graphtype'] not in ('Gráficas completas', 'Sensores por fermentador',
                                    'Promedio y desviación estándar')):
        window['checkresamp'].update(disabled=True)
        window['hourcombo'].update(visible=False)
        window['checkresamp'].update(visible=False)

    if (values['graphtype'] in ('Gráficas completas', 'Sensores por fermentador',
                                'Promedio y desviación estándar')):
        window['checkresamp'].update(disabled=False)
        window['hourcombo'].update(visible=True)
        window['checkresamp'].update(visible=True)
    if (values['graphtype'] not in ('Promedio y desviación estándar') and ferlist.count('Todos los fermentadores') > 0):
        todos = ferlist.remove('Todos los fermentadores')
        window['combofer'].update(
            value='Fermentador 1', values=ferlist)
    if (values['graphtype'] in ('Promedio y desviación estándar') and ferlist.count('Todos los fermentadores') == 0):
        ferlist.append('Todos los fermentadores')
        window['combofer'].update(
            value='Todos los fermentadores', values=ferlist)
    if (values['graphtype'] not in ('Perfil 3D', 'Cámara termica')):
        window['checkDate'].update(visible=True)
        window['checkDate'].update(disabled=False)
        window['-INICIALG-'].update(visible=True)
        window['-FINALG-'].update(visible=True)
        window['InicialButton'].update(visible=True)
        window['InicialText'].update(visible=True)
        window['FinalButton'].update(visible=True)
        window['FinalText'].update(visible=True)
        if (values['checkresamp'] != True):
            window['hourcombo'].update(value='12 hr', visible=False)
        if (values['checkresamp'] == True):
            window['hourcombo'].update(visible=True)
        if (values['checkDate'] != True):
            start_date = -1
            end_date = -1
            window['-INICIALG-'].update(visible=False)
            window['-FINALG-'].update(visible=False)
            window['InicialButton'].update(visible=False)
            window['InicialText'].update(visible=False)
            window['FinalButton'].update(visible=False)
            window['FinalText'].update(visible=False)
        if (values['checkDate'] == True):
            window['InicialText'].update(visible=True)
            window['-INICIALG-'].update(visible=True)
            window['InicialButton'].update(visible=True)
            window['FinalText'].update(visible=True)
            window['-FINALG-'].update(visible=True)
            window['FinalButton'].update(visible=True)

            if (values['-INICIALG-'] not in ('Elija una ->', start_date)):
                start_date = values['-INICIALG-']
                print(start_date)
            if (values['-FINALG-'] not in ('Elija una ->', end_date)):
                end_date = values['-FINALG-']
                print(end_date)

    if event == 'buttongraficar':
        plot = values['graphtype']
        resampling = values['hourcombo']
        request_dict = {'start_date': start_date, 'end_date': end_date,
                        'fermenter': fermenter, 'plot': plot, 'resampling': resampling}
        filename = request_plot(request_dict)
        window['ImagePlot'].update(filename=filename, visible=True)
        window.refresh()
        window.move_to_center()
        settings['ImagePlot'] = filename

window.close()
window.close()
window.close()
