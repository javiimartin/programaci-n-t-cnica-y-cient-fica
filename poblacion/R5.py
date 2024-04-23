#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 12:04:49 2023

@author: aulas
"""

import funciones as fun
import R2, R3
import matplotlib.pyplot as plt
import numpy as np

def graficar_evolucion_poblacion(comunidades_seleccionadas, poblacion_comunidades):
    # Asumimos que los años van de 2010 a 2017
    anos = np.arange(2010, 2018)

    # Configurar el gráfico de líneas
    plt.figure(figsize=(10, 8))

    for comunidad in comunidades_seleccionadas:
        # Convertir la serie de población total a un array de NumPy
        # Asumimos que la población total está en la primera mitad de la lista de cada comunidad
        poblacion_total = np.array(poblacion_comunidades[comunidad][:len(anos)])

        # Dibujar la línea para cada comunidad
        plt.plot(anos, poblacion_total, marker='o', label=fun.busca_comunidad(comunidad))

    # Añadir títulos y etiquetas
    plt.title('Evolución de la Población Total (2010-2017)')
    plt.xlabel('Año')
    plt.ylabel('Población')
    plt.legend(bbox_to_anchor=(1, 1))
    plt.grid(True)

    # Ajustar para que las etiquetas de los años se muestren correctamente
    plt.xticks(anos)

    # Guardar el gráfico en un archivo
    nombre_archivo_grafico = 'imagenes/grafico_lineas_poblacion.jpg'
    plt.savefig(nombre_archivo_grafico, bbox_inches='tight')
    plt.close()

    # Llamar a la función para incorporar el gráfico al archivo HTML
    fun.agregar_grafico_a_pagina_web("../imagenes/grafico_lineas_poblacion.jpg", "resultados/poblacionComAutonomas.html")



def main():
    # Leo los datos de cada provinciadel archivo csv
    datos_provincias = fun.leer_datos_csv("entradas/poblacionProvinciasHM2010-17.csv")
    # Leo las provincias y las comunidades autónomas de los ficheros html
    comunidades = fun.leer_comunidades_autonomas("entradas/comunidadesAutonomas.html")
    fun.actualizar_comunidades_provincias("entradas/comunidadAutonoma-Provincia.html", comunidades)
    # Calculo la población de cada comunidad autónoma
    poblacion_comunidades = R2.sumar_poblacion_comunidades(comunidades, datos_provincias)
    # Calculo las comunidades más pobladas
    comunidades = R3.calcular_comunidades_pobladas(poblacion_comunidades)
    # Llama a la función con el diccionario de población
    graficar_evolucion_poblacion(comunidades, poblacion_comunidades)
