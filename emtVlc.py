#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
# https://docs.python.org/3.6/library/urllib.html
import urllib.request  # for parsing URLs
import urllib.parse  # for opening and reading URLs
from bs4 import BeautifulSoup as bs

# VARS
path = "/route/to/path/emtVLC_conky/"
numParada = ""
numLinea = ""


# FUNCS

# Funcion que obtiene los datos de la web de EMT Vlc
def get_parada(numParada, linea='', adaptados=0, user='Anonimo', idioma='es'):
    emtVars = {'parada': numParada,
               'linea': numLinea,
               'adaptados': adaptados,
               'usuario': user,
               'idioma': idioma
               }
    emtVars = urllib.parse.urlencode(emtVars)
    emtArgs = emtVars.encode('ascii')
    emtUrl = 'https://www.emtvalencia.es/ciudadano/modules/mod_tiempo/busca_parada.php'
    req = urllib.request.Request(emtUrl, emtArgs)
    req.add_header("Content-type", "application/x-www-form-urlencoded")
    data = urllib.request.urlopen(req).read().decode('utf-8')
    return data


# Funcion para crear el objeto "soup"
def soup_html(numParada):
    # Datos que provienen de la funcion get_parada
    raw_data = get_parada(numParada)
    soup = bs(raw_data, "html.parser")
    return soup


# Funcion que devuelve los proximos buses
def prime_buses(numParada):
    # Objeto que proviene de la funcion soup_html
    data = soup_html(numParada)
    # Todos los span
    # spans = data.select('span')
    # Los span con la imagen de la linea
    # span_linea = data.find_all('span', {'class': 'imagenParada'})
    # Los span con el nombre de la linea y el tiempo
    span_tiempos = data.find_all('span', {'class': 'llegadaHome'})
    # Los img donde aparece la linea
    imgElem = data.select('img')
    buses = ''
    linea = ''
    # Bucle para mostrar linea y tiempo
    for span, img in zip(span_tiempos, imgElem):
        linea = img.get('title')
        show = span.getText(strip=True)
        # show = show.encode('utf-8')
        linea = str(linea)
        show = str(show)
        # print(linea, show)
        buses += linea + ': ' + show + "\n"
    if buses == 'None: PARADA NO CORRESPONDE\n':
        buses = "La linea " + numLinea + " no pasa por esta parada."
        return buses
    elif buses == 'None: LINEA NO ENCONTRADA\n':
        buses = "Todavia no hay estimaciones para la linea " + numLinea + " en esta parada."
        return buses
    if linea == 'None':
        buses = "Temporalmente fuera de servicio."
    if buses == '':
        buses += "No quedan buses... O la parada introducida no existe."
    return buses


if len(sys.argv) == 1:
    message = "No has introducido la parada!!"
else:
    numParada = numParada + sys.argv[1]
    if not numParada.isdigit():
        message = "No has introducido un número de parada válido."
    else:
        print("Parada: " + numParada)
        if len(sys.argv) > 2:
            numLinea = numLinea + sys.argv[2]
            with open(path+'numeroLineas.txt') as file:
                lineasEMT = file.read().splitlines()
                if numLinea in lineasEMT:
                    print("Linea: " + numLinea)
                else:
                    print("La linea \"" + numLinea + "\" no existe.")
                    numLinea = ''

        message = prime_buses(numParada)

print(message)
