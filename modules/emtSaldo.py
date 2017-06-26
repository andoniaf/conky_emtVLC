#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
# https://docs.python.org/3.6/library/urllib.html
import urllib.request  # for parsing URLs
import urllib.parse  # for opening and reading URLs
from bs4 import BeautifulSoup as bs

# VARS
numTarj = ""


# Funcion que obtiene los datos de la web de EMT Vlc
def get_saldo(numTarj, user='Anonimo', idioma='es'):
    emtVars = {'numero': numTarj,
               'usuario': user,
               'idioma': idioma
               }
    emtVars = urllib.parse.urlencode(emtVars)
    emtArgs = emtVars.encode('ascii')
    emtUrl = 'https://www.emtvalencia.es/ciudadano/modules/mod_saldo/busca_saldo.php'
    req = urllib.request.Request(emtUrl, emtArgs)
    req.add_header("Content-type", "application/x-www-form-urlencoded")
    data = urllib.request.urlopen(req).read().decode('utf-8')
    return data


# Funcion para crear el objeto "soup"
def soup_html(numTarj):
    # Datos que provienen de la funcion get_saldo
    raw_data = get_saldo(numTarj)
    soup = bs(raw_data, "html.parser")
    return soup


# Funcion que devuelve el saldo
def prime_saldo(numTarj):
    # Objeto que proviene de la funcion soup_html
    data = soup_html(numTarj)
    raw_viajes = data.select('strong')
    # Comprobación pdte de tener nombre
    if not raw_viajes:
        raw_error = data.select('span')
        error = raw_error[0].getText()
        mensaje = 'ERROR: ' + error
    else:
        raw_ultUso = data.select('br')[4]
        viajes = raw_viajes[0].getText()
        ultUso = raw_ultUso.getText().splitlines()[0]
        nota = 'En el caso de haberla utilizado o recargado con posterioridad a la fecha y hora ' \
               'indicada, el número de viajes será diferente al mostrado. '
        mensaje = 'Tarjeta: ' + numTarj + '\n'
        mensaje += viajes + '\n'
        mensaje += ultUso + '\n'
        mensaje += nota
    return mensaje

