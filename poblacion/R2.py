#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 12:04:25 2023

@author: Javier
Usando el listado de comunidades autónomas de comunidadesAutonomas.html, así como de las provincias de cada comunidad
autónoma del fichero comunidadAutonoma-Provincia.html y los datos de poblacionProvinciasHM2010-17.csv, hay que generar 
una página web poblacionComAutonomas.html con una tabla con los valores de población de cada comunidad autónoma en cada 
año de 2010 a 2017, indicando también los valores desagregados por sexos 
"""

import funciones as fun
import numpy as np
import locale

def sumar_poblacion_comunidades(comunidades_provincias, datos_provincias):
    poblacion_comunidades = {}

    for comunidad, provincias in comunidades_provincias.items():
        if provincias is not None:
            total_poblacion = np.zeros(3 * fun.NUM_ANIOS)
            for codigo_provincia, nombre_provincia in provincias:
                clave_provincia = f"{codigo_provincia} {nombre_provincia}"
                if clave_provincia in datos_provincias:
                    poblacion_provincia = np.array(datos_provincias[clave_provincia])
                    total_poblacion += poblacion_provincia
                else:
                    print(f"Advertencia: La provincia {clave_provincia} no se encontró en los datos de población.")
            poblacion_comunidades[comunidad] = total_poblacion
        else:
            print(f"Advertencia: La comunidad autónoma {comunidad} no tiene provincias asociadas.")

    return poblacion_comunidades


def generar_pagina_web(poblacion_comunidades):
    nombre_archivo = 'resultados/poblacionComAutonomas.html'
    locale.setlocale(locale.LC_ALL, '')

    with open(nombre_archivo, 'w', encoding='utf-8') as f:
        f.write('<!DOCTYPE html>\n<html>\n<head>\n')
        f.write('<title>Población por Comunidades Autónomas</title>\n')
        f.write('<link rel="stylesheet" type="text/css" href="../entradas/estilo.css">\n')
        f.write('</head>\n<body>\n')
        f.write('<h1>Población por Comunidades Autónomas</h1>\n')
        f.write('<table>\n')

        # Encabezado de la tabla
        f.write('<tr><th rowspan="2">Comunidad Autónoma</th>')
        for tipo_poblacion in ["Total", "Hombres", "Mujeres"]:
            f.write(f'<th colspan="{fun.NUM_ANIOS}">{tipo_poblacion}</th>')
        f.write('</tr>\n<tr>')
        for _ in range(3):  # Tres veces porque hay tres tipos de población: Total, Hombres, Mujeres
            for i in range(fun.NUM_ANIOS):
                f.write(f'<th>{2017 - i}</th>')
        f.write('</tr>\n')

        # Datos de las comunidades autónomas
        for cod_comunidad, datos in poblacion_comunidades.items():
            f.write(f'<tr><td>{fun.busca_comunidad(cod_comunidad)}</td>')
            for dato in datos:
                f.write(f'<td>{locale.format_string("%.0f", dato, grouping=True)}</td>')
            f.write('</tr>\n')

        f.write('</table>\n</body>\n</html>')


def main():
    # Leo los datos de cada provinciadel archivo csv
    datos_provincias = fun.leer_datos_csv("entradas/poblacionProvinciasHM2010-17.csv")
    # Leo las provincias y las comunidades autónomas de los ficheros html
    comunidades = fun.leer_comunidades_autonomas("entradas/comunidadesAutonomas.html")
    fun.actualizar_comunidades_provincias("entradas/comunidadAutonoma-Provincia.html", comunidades)
    # Calculo la población de cada comunidad autónoma
    solucion = sumar_poblacion_comunidades(comunidades, datos_provincias)
    # Genero la página web con los resultados
    generar_pagina_web(solucion)

if __name__ == "__main__":
    main()