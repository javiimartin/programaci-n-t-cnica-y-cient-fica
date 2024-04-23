#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 12:04:05 2023

@author: Javier 
Calcular la variación de la población por provincias desde el año 2011 a 2017 en términos absolutos 
y relativos generando una página web que contenga una tabla mostrando los resultados
"""

import funciones as fun
import numpy as np
import locale


def calcular_variacion(datos_provincias):
    variacion_absoluta = {}
    variacion_relativa = {}
    
    for provincia, poblacion in datos_provincias.items():
        # Convertir la lista de población a un array de NumPy
        poblacion_np = np.array(poblacion[:fun.NUM_ANIOS])

        # Calcular la variación absoluta usando la diferencia entre elementos adyacentes
        variacion_absoluta_provincia = np.diff(poblacion_np) * -1

        # Calcular la variación relativa
        variacion_relativa_provincia = (variacion_absoluta_provincia / poblacion_np[1:]) * 100

        # Redondear la variación relativa 
        variacion_relativa_provincia = np.round(variacion_relativa_provincia, 2)

        # Guardar los resultados en los diccionarios convertidos a listas
        variacion_absoluta[provincia] = variacion_absoluta_provincia.tolist()
        variacion_relativa[provincia] = variacion_relativa_provincia.tolist()
        
    return variacion_absoluta, variacion_relativa



def generar_pagina_web(variacion_absoluta, variacion_relativa):
    nombre_archivo='resultados/variacionProvincias.html'
    num_anios = len(next(iter(variacion_absoluta.values())))
    locale.setlocale(locale.LC_ALL,'')
    
    with open(nombre_archivo, 'w', encoding='utf-8') as f:
        f.write('<!DOCTYPE html>\n<html>\n<head>\n')
        f.write('<title>Variación de Población por Provincias</title>\n')
        f.write('<link rel="stylesheet" type="text/css" href="../entradas/estilo.css">\n')
        f.write('</head>\n<body>\n')
        f.write('<h1>Variación de Población por Provincias</h1>\n')
        f.write('<table>\n')
        
        # Encabezado de la tabla
        f.write('<tr><th rowspan="2">Provincia</th><th colspan="{}">Variación Absoluta</th><th colspan="{}">Variación Relativa </th></tr>\n'.format(num_anios, num_anios))
        f.write('<tr>')
        for tipo_variacion in range(2):  # Dos veces porque hay dos tipos de variación: absoluta y relativa
            for i in range(2017, 2017 - num_anios, -1):
                f.write(f'<th>{i}</th>')
        f.write('</tr>\n')
        
        # Datos de las provincias
        for provincia in variacion_absoluta:
            f.write(f'<tr><td>{provincia}</td>')
            for var_abs in variacion_absoluta[provincia]:
                f.write(f'<td>{locale.format_string("%.0f", var_abs, grouping=True)}</td>')
            for var_rel in variacion_relativa[provincia]:
                f.write(f'<td>{locale.format_string("%.2f", var_rel, grouping=True)}</td>')
            f.write('</tr>\n')
        
        f.write('</table>\n</body>\n</html>')




def main():
    datos_provincias = fun.leer_datos_csv("entradas/poblacionProvinciasHM2010-17.csv")
    absoluta, relativa = calcular_variacion(datos_provincias)
    generar_pagina_web(absoluta, relativa)
    
    
    
    
