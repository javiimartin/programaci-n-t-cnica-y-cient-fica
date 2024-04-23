#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 12:02:54 2023

@author: aulas
"""

import csv
import numpy as np
from bs4 import BeautifulSoup

# Constantes
NUM_ANIOS = 8

"""
Función para contar el número de provincias dado un archivo html
"""
def contar_provincias(html_filename):
   
    with open(html_filename, 'r', encoding='utf-8') as htmlfile:
        soup = BeautifulSoup(htmlfile, 'html.parser')
        # Selecciona todas las celdas de la cuarta columna de la tabla con clase 'miTabla'
        provincias = soup.select('table.miTabla tr td:nth-of-type(4)')
        # Filtra las celdas que no estén vacías
        provincias_no_vacias = [provincia for provincia in provincias if provincia.text.strip() != '']
        return len(provincias_no_vacias)
    
"""
Función para leer los datos desde un archivo csv
Usamos la variable FILAS_IRRELEVANTES para saltarnos las primeras filas que no contienen información útil
Con la función contar provincias sabemos cuantas provincias tenemos que leer
"""
def leer_datos_csv(ruta_archivo):
    # Inicializar el diccionario para guardaar los datos
    datos_provincias = {}

    # Abrimos el archivo csv
    with open(ruta_archivo, 'r', encoding='utf-8') as csvfile:
        # Crear un lector de csv
        lector = csv.reader(csvfile, delimiter=';')
        # Saltar las lineas irrelevantes
        for fila in lector:
            if fila[0] == "Total Nacional":
                break
            
        # Leer las filas de provinvias
        while fila[0] != "Notas:": 
            # Codigo y nombre de la provincia en la primera columna
            codigo_nombre_provincia = fila[0]
            # Las siguientes 3*NUM_ANIOS columnas es la poblacion total, masculina y femenina
            datos_poblacion = np.array(fila[1:1 + 3 * NUM_ANIOS], dtype=float)
            datos_provincias[codigo_nombre_provincia] = datos_poblacion
            fila = next(lector)
    
    return datos_provincias


def leer_comunidades_autonomas(ruta_archivo):
    comunidades_autonomas = {}

    # Abrir y leer el archivo HTML
    with open(ruta_archivo, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    # Encontrar la tabla en el archivo HTML
    tabla = soup.find('table')
    if tabla is None:
        print("No se encontró ninguna tabla en el archivo.")
        return comunidades_autonomas

    # Iterar sobre las filas de la tabla
    for fila in tabla.find_all('tr')[1:]:  # [1:] para saltar la fila de encabezados
        columnas = fila.find_all('td')
        if len(columnas) >= 2:
            codigo = columnas[0].text.strip()
            comunidades_autonomas[codigo] = None  # Inicializar con None, los datos se llenarán después

    return comunidades_autonomas


def actualizar_comunidades_provincias(ruta_archivo, comunidades_autonomas):
    # Abrir y leer el archivo HTML
    with open(ruta_archivo, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    # Encontrar la tabla en el archivo HTML
    tabla = soup.find('table')
    if tabla is None:
        print("No se encontró ninguna tabla en el archivo.")
        return

    # Iterar sobre las filas de la tabla
    for fila in tabla.find_all('tr')[1:]:  # [1:] para saltar la fila de encabezados
        columnas = fila.find_all('td')
        if len(columnas) >= 4:
            codigo_comunidad = columnas[0].text.strip()
            codigo_provincia = columnas[2].text.strip()
            nombre_provincia = columnas[3].text.strip()

            clave_comunidad = f"{codigo_comunidad}"

            # Si la comunidad autónoma ya está en el diccionario, se añade la provincia a su lista
            if clave_comunidad in comunidades_autonomas:
                if comunidades_autonomas[clave_comunidad] is None:
                    comunidades_autonomas[clave_comunidad] = []
                comunidades_autonomas[clave_comunidad].append((codigo_provincia, nombre_provincia))
            else:
                print(f"Advertencia: La comunidad autónoma {clave_comunidad} no está en el diccionario.")


"""
Función que devuelve el nombre de una comunidad autónoma a partir de su código
"""
def busca_comunidad(codigo):
    ruta_archivo = "entradas/comunidadesAutonomas.html"

    # Abrir y leer el archivo HTML
    with open(ruta_archivo, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
    
    # Encontrar la tabla en el archivo HTML
    tabla = soup.find('table')
    if tabla is None:
        print("No se encontró ninguna tabla en el archivo.")
    
    # Iterar sobre las filas de la tabla
    for fila in tabla.find_all('tr')[1:]:  # [1:] para saltar la fila de encabezados
        columnas = fila.find_all('td')
        if len(columnas) >= 2:
            if codigo == columnas[0].text.strip():
                nombre = columnas[1].text.strip()
                clave = f"{codigo} {nombre}"

    return clave
    
def agregar_grafico_a_pagina_web(nombre_archivo_imagen, nombre_archivo_html):
    codigo_html_img = f'\n<div><img src="{nombre_archivo_imagen}" height="500" width="500" border="1"></div>\n'
    
    with open(nombre_archivo_html, 'a', encoding='utf-8') as f:
        f.write("<p>")
        f.write(codigo_html_img)
        f.write("</p>")
    

def main():
    datos = leer_comunidades_autonomas("entradas/comunidadesAutonomas.html")
    actualizar_comunidades_provincias("entradas/comunidadAutonoma-Provincia.html", datos)
    print(datos)


if __name__ == "__main__":
    main()
    
    
    

