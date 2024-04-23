#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 12:04:41 2023

@author: aulas
"""

import funciones as fun
import numpy as np
import R2
import locale

def calcular_variacion(datos_provincias):
    absoluta_hombres = {}
    relativa_hombres = {}
    absoluta_mujeres = {}
    relativa_mujeres = {}
    
    for provincia, poblacion in datos_provincias.items():
        # Convertimos la lista de población a un array de NumPy
        poblacion_np = np.array(poblacion)

        # Calculamos la variación absoluta y relativa para hombres
        variacion_absoluta_hombres = np.diff(poblacion_np[fun.NUM_ANIOS:2*fun.NUM_ANIOS]) * -1
        variacion_relativa_hombres = (variacion_absoluta_hombres / poblacion_np[fun.NUM_ANIOS+1:2*fun.NUM_ANIOS]) * 100

        # Calculamos la variación absoluta y relativa para mujeres
        variacion_absoluta_mujeres = np.diff(poblacion_np[2*fun.NUM_ANIOS:3*fun.NUM_ANIOS]) * -1
        variacion_relativa_mujeres = (variacion_absoluta_mujeres / poblacion_np[2*fun.NUM_ANIOS+1:3*fun.NUM_ANIOS]) * 100

        # Guardar los resultados en los diccionarios
        absoluta_hombres[provincia] = variacion_absoluta_hombres.tolist()
        relativa_hombres[provincia] = np.round(variacion_relativa_hombres, 2).tolist()
        absoluta_mujeres[provincia] = variacion_absoluta_mujeres.tolist()
        relativa_mujeres[provincia] = np.round(variacion_relativa_mujeres, 2).tolist()
        
    return absoluta_hombres, relativa_hombres, absoluta_mujeres, relativa_mujeres



def generar_pagina_web(absoluta_hombres, relativa_hombres, absoluta_mujeres, relativa_mujeres):
    nombre_archivo = 'resultados/variacionComAutonomas.html'
    locale.setlocale(locale.LC_ALL, '')

    with open(nombre_archivo, 'w', encoding='utf-8') as f:
        f.write('<!DOCTYPE html>\n<html>\n<head>\n')
        f.write('<title>Variación de Población por Provincias y Sexo</title>\n')
        f.write('<link rel="stylesheet" type="text/css" href="../entradas/estilo.css">\n')
        f.write('</head>\n<body>\n')
        f.write('<h1>Variación de Población por Provincias y Sexo</h1>\n')
        f.write('<table>\n')

        # Encabezado de la tabla
        f.write('<tr><th rowspan="3">Provincia</th>')
        f.write('<th colspan="{}">Variación Absoluta </th>'.format(2*fun.NUM_ANIOS-2))
        f.write('<th colspan="{}">Variación Relativa </th></tr>\n'.format(2*fun.NUM_ANIOS-1))
        
        f.write('<tr><th colspan="{}"> Hombres </th>'.format(fun.NUM_ANIOS-1))
        f.write('<th colspan="{}"> Mujeres </th>'.format(fun.NUM_ANIOS-1))
        f.write('<th colspan="{}"> Hombres </th>'.format(fun.NUM_ANIOS-1))
        f.write('<th colspan="{}"> Mujeres </th></tr>\n'.format(fun.NUM_ANIOS-1))
        
        

        f.write('<tr>')
        for _ in range(4):  # Dos veces por sexo
            for i in range(2017, 2017 - fun.NUM_ANIOS+1, -1):
                f.write(f'<th>{i}</th>')
        f.write('</tr>\n')

        # Datos de las provincias
        for provincia in absoluta_hombres:
            f.write(f'<tr><td>{fun.busca_comunidad(provincia)}</td>')
            for var_abs in absoluta_hombres[provincia]:
                f.write(f'<td>{locale.format_string("%.0f", var_abs, grouping=True)}</td>')
            for var_abs in absoluta_mujeres[provincia]:
                f.write(f'<td>{locale.format_string("%.0f", var_abs, grouping=True)}</td>')
            for var_rel in relativa_hombres[provincia]:
                f.write(f'<td>{locale.format_string("%.2f", var_rel, grouping=True)}</td>')
            for var_rel in relativa_mujeres[provincia]:
                f.write(f'<td>{locale.format_string("%.2f", var_rel, grouping=True)}</td>')
            f.write('</tr>\n')

        f.write('</table>\n</body>\n</html>')



def main():
    # Leo los datos de cada provinciadel archivo csv
    datos_provincias = fun.leer_datos_csv("entradas/poblacionProvinciasHM2010-17.csv")
    # Leo las provincias y las comunidades autónomas de los ficheros html
    comunidades = fun.leer_comunidades_autonomas("entradas/comunidadesAutonomas.html")
    fun.actualizar_comunidades_provincias("entradas/comunidadAutonoma-Provincia.html", comunidades)
    # Calculo la población de cada comunidad autónoma
    datos_comunidades = R2.sumar_poblacion_comunidades(comunidades, datos_provincias)
    
    absoluta_hombres, relativa_hombres, absoluta_mujeres, relativa_mujeres = calcular_variacion(datos_comunidades)
    #print(datos_provincias)
    #print(absoluta_hombres["01"])
    #print(relativa_mujeres["01"])
    generar_pagina_web(absoluta_hombres, relativa_hombres, absoluta_mujeres, relativa_mujeres)
    
    
    

if __name__ == "__main__":
    main()
    