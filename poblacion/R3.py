#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 12:04:33 2023

@author: aulas
"""

import funciones as fun
import matplotlib.pyplot as plt
import numpy as np
import R2

#Función para calcular las comunidades autónomas más pobladas
def calcular_comunidades_pobladas(poblacion_comunidades):
    poblacion_media_comunidades = {}

    for comunidad, datos in poblacion_comunidades.items():
        datos_np = np.array(datos[:fun.NUM_ANIOS])
        poblacion_media = np.mean(datos_np)
        poblacion_media_comunidades[comunidad] = poblacion_media

    comunidades_seleccionadas = dict(sorted(poblacion_media_comunidades.items(), key=lambda item: item[1], reverse=True)[:10])

    return comunidades_seleccionadas

    

def graficar_poblacion(comunidades_seleccionadas, poblacion_comunidades):
    datos_comunidades_seleccionadas = {comunidad: np.array(poblacion_comunidades[comunidad]) for comunidad in comunidades_seleccionadas}

    comunidades = [fun.busca_comunidad(comunidad) for comunidad in datos_comunidades_seleccionadas.keys()]
    
    poblacion_hombres = [datos_comunidades_seleccionadas[comunidad][fun.NUM_ANIOS] for comunidad in datos_comunidades_seleccionadas]
    poblacion_mujeres = [datos_comunidades_seleccionadas[comunidad][2*fun.NUM_ANIOS] for comunidad in datos_comunidades_seleccionadas]

    ind = np.arange(len(comunidades)) * 1.5
    width = 0.35

    plt.bar(ind - width/2, poblacion_hombres, width, label='Hombres', color='blue')
    plt.bar(ind + width/2, poblacion_mujeres, width, label='Mujeres', color='red')

    plt.ylabel('Población')
    plt.title('Población por sexo en el año 2017 (CCAA)')
    plt.xticks(ind, comunidades, rotation='vertical')
    plt.legend()

    nombre_archivo_grafico = 'imagenes/poblacion_comunidades.jpg'
    plt.savefig(nombre_archivo_grafico, bbox_inches='tight')
    plt.close()

    fun.agregar_grafico_a_pagina_web("../imagenes/poblacion_comunidades.jpg", "resultados/poblacionComAutonomas.html")





def main():
    # Leo los datos de cada provinciadel archivo csv
    datos_provincias = fun.leer_datos_csv("entradas/poblacionProvinciasHM2010-17.csv")
    # Leo las provincias y las comunidades autónomas de los ficheros html
    comunidades = fun.leer_comunidades_autonomas("entradas/comunidadesAutonomas.html")
    fun.actualizar_comunidades_provincias("entradas/comunidadAutonoma-Provincia.html", comunidades)
    # Calculo la población de cada comunidad autónoma
    poblacion_comunidades = R2.sumar_poblacion_comunidades(comunidades, datos_provincias)
    # Calculo las comunidades más pobladas
    comunidades = calcular_comunidades_pobladas(poblacion_comunidades)
    # Llama a la función con el diccionario de población
    graficar_poblacion(comunidades, poblacion_comunidades)
    
    
if __name__ == "__main__":
    main()
    
    
    
    
    
