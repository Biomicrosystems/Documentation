#Screen is 240x320
scrn_height = 240
scrn_width = 320

#sensor is an 8x8 grid so lets do a square
map_height = min(scrn_height,scrn_width)
map_width = min(scrn_height,scrn_width)

def posBotonEsquina(pos, dim):
    rec = [pos[0]-dim[0]/2, pos[1]-dim[1]/2]
    return rec

def bonotesMAinScreen(pygame, botones):
    #Cargamos las imagenes que serviran como botones
    play_boton_imagen = pygame.image.load("imagenes/play.png")
    stop_boton_imagen = pygame.image.load("imagenes/stop.png")
    config_boton_imagen = pygame.image.load("imagenes/settings.jpeg")
    csv_start_imagen = pygame.image.load("imagenes/record.png")
    csv_stop_imagen = pygame.image.load("imagenes/StopRecord.png")
    swicth_on_imagen = pygame.image.load("imagenes/swicthOn.png")
    swicth_off_imagen = pygame.image.load("imagenes/swicthOff.png")

    #Se escalan las imagenes cargadas
    tam_boton = (scrn_width - map_width)/2
    play_boton_imagen = pygame.transform.scale(play_boton_imagen, [tam_boton, tam_boton])
    stop_boton_imagen = pygame.transform.scale(stop_boton_imagen, [tam_boton, tam_boton])
    config_boton_imagen = pygame.transform.scale(config_boton_imagen, [tam_boton, tam_boton])
    csv_start_imagen = pygame.transform.scale(csv_start_imagen, [tam_boton, tam_boton])
    csv_stop_imagen = pygame.transform.scale(csv_stop_imagen, [tam_boton, tam_boton])
    swicth_off_imagen = pygame.transform.scale(swicth_off_imagen, [tam_boton, tam_boton])
    swicth_on_imagen = pygame.transform.scale(swicth_on_imagen, [tam_boton, tam_boton])

    csv_start_imagen.set_alpha(20)

    #Se crea el rectangulo de cada boton
    r_boton_play = play_boton_imagen.get_rect()
    r_boton_confg = config_boton_imagen.get_rect()
    r_boton_csv = csv_start_imagen.get_rect()
    r_boton_on = swicth_on_imagen.get_rect()


    #Asignacion de posiciones
    #top_left = map_width + int(((scrn_width - map_width) - tam_boton )/2)
    top_left = scrn_width - tam_boton
    top_up = scrn_height/10
    boton_separacion = scrn_height/4
    r_boton_play.topleft = [top_left, top_up ]
    r_boton_csv.topleft = [top_left, top_up + boton_separacion]
    r_boton_confg.topleft = [top_left, top_up + boton_separacion*2]
    r_boton_on.topleft = [top_left, top_up + boton_separacion*3]

    botones.append({'imagen': play_boton_imagen, 'imagen_dos': stop_boton_imagen, 'rect': r_boton_play, 'selected': False, 'texto1': ["Video"], 'texto2': ["Video"]})
    botones.append({'imagen': csv_start_imagen, 'imagen_dos': csv_stop_imagen, 'rect': r_boton_csv, 'selected': False, 'texto1': ["CSV"], 'texto2': ["CSV"]})
    botones.append({'imagen': config_boton_imagen, 'imagen_dos': config_boton_imagen, 'rect': r_boton_confg, 'selected': False,'texto1': [""], 'texto2': [""]})
    botones.append({'imagen': swicth_off_imagen, 'imagen_dos': swicth_on_imagen, 'rect': r_boton_on, 'selected': True,'texto1': ["Temp"], 'texto2': ["Temp"]})

##############################################################################   Botones configuracion   #######################################################
    
def botonesSettingScreen(pygame, botonesConfig):
    # Variables interfaz
    widthBoton = 55
    heightBoton = 55

    posMin = (53, 185)
    posMax = (53, 75)
    posCal = (160, 75)
    posSalir = (267, 75)
    posApa = (267, 185)

    # Cargamos las imagenes que serviran como botones
    minTem_boton_imagen = pygame.image.load("imagenes/downArrow.png")
    maxTem_boton_imagen = pygame.image.load("imagenes/upArrow.png")
    calibra_boton_imagen = pygame.image.load("imagenes/calibration.png")
    salir_boton_imagen = pygame.image.load("imagenes/quit.png")
    apagar_boton_imagen = pygame.image.load("imagenes/shutdown.png")

    # Se escalan las imagenes cargadas
    minTem_boton_imagen = pygame.transform.scale(minTem_boton_imagen, [widthBoton, heightBoton])
    maxTem_boton_imagen = pygame.transform.scale(maxTem_boton_imagen, [widthBoton, heightBoton])
    calibra_boton_imagen = pygame.transform.scale(calibra_boton_imagen, [widthBoton, heightBoton])
    salir_boton_imagen = pygame.transform.scale(salir_boton_imagen, [widthBoton, heightBoton])
    apagar_boton_imagen = pygame.transform.scale(apagar_boton_imagen, [widthBoton, heightBoton])

    # Se crea el rectangulo de cada boton
    r_boton_minTem = minTem_boton_imagen.get_rect()
    r_boton_maxTem = maxTem_boton_imagen.get_rect()
    r_boton_calibra = calibra_boton_imagen.get_rect()
    r_boton_salir = salir_boton_imagen.get_rect()
    r_boton_apagar = apagar_boton_imagen.get_rect()


    # Asignacion de posiciones
    r_boton_maxTem.topleft = posBotonEsquina(posMax, (widthBoton, heightBoton))
    r_boton_minTem.topleft = posBotonEsquina(posMin, (widthBoton, heightBoton))

    r_boton_calibra.topleft = posBotonEsquina(posCal, (widthBoton, heightBoton))

    r_boton_salir.topleft = posBotonEsquina(posSalir, (widthBoton, heightBoton))
    r_boton_apagar.topleft = posBotonEsquina(posApa, (widthBoton, heightBoton))

    # Se agregan los botones con sus respectivas propiedades
    botonesConfig.append(
        {'imagen': maxTem_boton_imagen, 'rect': r_boton_maxTem, 'selected': False, 'texto': ["Maxima temp"],
         'pos': posMax})
    botonesConfig.append(
        {'imagen': calibra_boton_imagen, 'rect': r_boton_calibra, 'selected': False, 'texto': ["Calibrar"],
         'pos': posCal})
    botonesConfig.append(
        {'imagen': salir_boton_imagen, 'rect': r_boton_salir, 'selected': False, 'texto': ["Salir"], 'pos': posSalir})
    botonesConfig.append(
        {'imagen': minTem_boton_imagen, 'rect': r_boton_minTem, 'selected': False, 'texto': ["Minima temp"],
         'pos': posMin})
    botonesConfig.append(
        {'imagen': apagar_boton_imagen, 'rect': r_boton_apagar, 'selected': False, 'texto': ["Apagar"], 'pos': posApa})

############################################################### Botones ajuste limites ######################################################################

def botonesLimScreen(pygame, botonesMaximo):
    widthBoton = 80
    heightBoton = 80

    posMas = (267, 150)
    posMenos = (53, 150)
    posSave = (30, 30)

    # Cargamos las imagenes que serviran como botones
    menos_boton_imagen = pygame.image.load("imagenes/back.png")
    mas_boton_imagen = pygame.image.load("imagenes/fordward.png")
    save_boton_imagen = pygame.image.load("imagenes/save.png")

    # Se escalan las imagenes cargadas
    menos_boton_imagen = pygame.transform.scale(menos_boton_imagen, [widthBoton, heightBoton])
    mas_boton_imagen = pygame.transform.scale(mas_boton_imagen, [widthBoton, heightBoton])
    save_boton_imagen = pygame.transform.scale(save_boton_imagen, [40, 40])

    # Se crea el rectangulo de cada boton
    r_boton_mas = mas_boton_imagen.get_rect()
    r_boton_menos = menos_boton_imagen.get_rect()
    r_boton_save = save_boton_imagen.get_rect()


    # Asignacion de posiciones
    r_boton_mas.topleft = posBotonEsquina(posMas, (widthBoton, heightBoton))
    r_boton_menos.topleft = posBotonEsquina(posMenos, (widthBoton, heightBoton))
    r_boton_save.topleft = [10, 10]

    botonesMaximo.append(
        {'imagen': mas_boton_imagen, 'rect': r_boton_mas, 'selected': False, 'texto': [""], 'pos': posMas})
    botonesMaximo.append(
        {'imagen': menos_boton_imagen, 'rect': r_boton_menos, 'selected': False, 'texto': [""], 'pos': posMenos})
    botonesMaximo.append(
        {'imagen': save_boton_imagen, 'rect': r_boton_save, 'selected': False, 'texto': [""], 'pos': posSave})

######################################################################### Botones Calibracion ####################################################
def botonesCalScreen(pygame, botonesCalibracion):
    widthBoton = 80
    heightBoton = 80

    margen = 0

    posMas = [map_width - margen - (widthBoton / 2), 200]
    posMenos = [margen + (widthBoton / 2), 200]
    posSave = [30, 30]
    posReturn = [scrn_width - 30, 30]
    posObturador = [290, 120]
    posReTry = [290,200]
    posVarCalibracion = [scrn_height / 2, 200]

    # Cargamos las imagenes que serviran como botones
    menos_boton_imagen = pygame.image.load("imagenes/back.png")
    menos_boton_imagen_dos = pygame.image.load("imagenes/backGray.png")
    mas_boton_imagen = pygame.image.load("imagenes/fordward.png")
    mas_boton_imagen_dos = pygame.image.load("imagenes/fordwardGray.png")
    save_boton_imagen = pygame.image.load("imagenes/save.png")
    save_boton_imagen_dos = pygame.image.load("imagenes/saveUnavailable.png")
    return_boton_imagen = pygame.image.load("imagenes/return.png")
    shutter_boton_imagen = pygame.image.load("imagenes/shutter.png")
    shutter_boton_imagen_dos = pygame.image.load("imagenes/checkedShutter.png")
    reTry_boton_imagen = pygame.image.load("imagenes/reTry.png")
    reTry_boton_imagen_dos = pygame.image.load("imagenes/empty.png")

    # Se escalan las imagenes cargadas
    menos_boton_imagen = pygame.transform.scale(menos_boton_imagen, [widthBoton, heightBoton])
    menos_boton_imagen_dos = pygame.transform.scale(menos_boton_imagen_dos, [widthBoton, heightBoton])

    mas_boton_imagen = pygame.transform.scale(mas_boton_imagen, [widthBoton, heightBoton])
    mas_boton_imagen_dos = pygame.transform.scale(mas_boton_imagen_dos, [widthBoton, heightBoton])

    save_boton_imagen = pygame.transform.scale(save_boton_imagen, [40, 40])
    save_boton_imagen_dos = pygame.transform.scale(save_boton_imagen_dos, [40, 40])

    return_boton_imagen = pygame.transform.scale(return_boton_imagen, [40, 40])
    shutter_boton_imagen = pygame.transform.scale(shutter_boton_imagen, [60, 60])
    shutter_boton_imagen_dos = pygame.transform.scale(shutter_boton_imagen_dos, [60, 60])

    reTry_boton_imagen = pygame.transform.scale(reTry_boton_imagen, [40,40])
    reTry_boton_imagen_dos = pygame.transform.scale(reTry_boton_imagen_dos, [40,40])

    # Se crea el rectangulo de cada boton
    r_boton_mas = mas_boton_imagen.get_rect()
    r_boton_menos = menos_boton_imagen.get_rect()
    r_boton_save = save_boton_imagen.get_rect()
    r_boton_shutter = shutter_boton_imagen.get_rect()
    r_boton_return = return_boton_imagen.get_rect()
    r_boton_reTry = reTry_boton_imagen.get_rect()


    # Asignacion de posiciones
    r_boton_mas.center = posMas
    r_boton_menos.center = posMenos
    r_boton_save.center = posSave
    r_boton_shutter.center = posObturador
    r_boton_return.center = posReturn
    r_boton_reTry.center = posReTry

    botonesCalibracion.append(
        {'imagen': save_boton_imagen, 'imagen_dos': save_boton_imagen_dos, 'rect': r_boton_save, 'selected': False, 'pos': posSave, 'habilitado': False})
    botonesCalibracion.append(
        {'imagen': return_boton_imagen, 'imagen_dos': return_boton_imagen, 'rect': r_boton_return, 'selected': False, 'pos': posReturn, 'habilitado': True})
    botonesCalibracion.append(
        {'imagen': menos_boton_imagen, 'imagen_dos': menos_boton_imagen_dos, 'rect': r_boton_menos, 'selected': False, 'pos': posMenos, 'habilitado': False})
    botonesCalibracion.append(
        {'imagen': mas_boton_imagen, 'imagen_dos': mas_boton_imagen_dos, 'rect': r_boton_mas, 'selected': False, 'pos': posMas, 'habilitado': False})
    botonesCalibracion.append(
        {'imagen': shutter_boton_imagen, 'imagen_dos': shutter_boton_imagen_dos, 'rect': r_boton_shutter, 'selected': False, 'pos': posObturador, 'habilitado': True})
    botonesCalibracion.append(
        {'imagen': reTry_boton_imagen, 'imagen_dos': reTry_boton_imagen_dos, 'rect': r_boton_reTry, 'selected': False, 'pos': posReTry, 'habilitado': False})

# def text_box():
#     global active, text, done, color
#
#     while not done:
#
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 done = True
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 # If the user clicked on the input_box rect.
#                 if input_box.collidepoint(event.pos):
#                     # Toggle the active variable.
#                     active = not active
#                 else:
#                     active = False
#                 # Change the current color of the input box.
#                 color = color_active if active else color_inactive
#             if event.type == pygame.KEYDOWN:
#                 if active:
#                     if event.key == pygame.K_RETURN:
#                         velocidad(text)
#                         print(text)
#                         text = ''
#                         pygame.draw.rect(Display, Blanco, input_box, 0)
#
#
#                     elif event.key == pygame.K_BACKSPACE:
#                         text = text[:-1]
#                     else:
#                         letra = event.unicode
#                         if letra.isdigit():
#                             text += letra
#
#
#         label = font.render("Velocidad:", True, color)
#         Display.blit(label, [20, dimY-32])
#
#
#         label = font.render("X: ", True, color)
#         Display.blit(label, [340, dimY-50])
#
#
#         label = font.render("Y: ", True, color)
#         Display.blit(label, [340, dimY-25])
#
#         txt_surface = font.render(text, True, Negro)
#         # Resize the box if the text is too long.
#         width = max(200, txt_surface.get_width() + 10)
#         input_box.w = width
#         # Blit the text.
#         Display.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
#         # Blit the input_box rect.
#         pygame.draw.rect(Display, color, input_box, 2)
#
#         pygame.display.flip()
