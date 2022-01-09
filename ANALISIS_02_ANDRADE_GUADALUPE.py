#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  8 17:14:07 2022

@author: Guadalupe Andrade, gupeanzu@gmail.com
"""

import pandas as pd
#%%

synergy_dataframe = pd.read_csv('synergy_logistics_database.csv', index_col=0,
                                encoding='utf-8', 
                                parse_dates=[4, 5])
#%%
"""
  ### Actividad que se pide.
  
Synergy logistics está considerando la posibilidad de enfocar sus esfuerzos en 
las 10 rutas más demandadas. Acorde a los flujos de importación y exportación, 
¿cuáles son esas 10 rutas?

"""

# resultado: combinación entre 'product', 'transport_mode' 'origin' y 'destination'.
combinaciones = synergy_dataframe.groupby(by=['origin', 'destination',
                                               'transport_mode', 'product'])

# tomando en cuenta el grupo de los datos con base a columnas que se indicaron, 
#procedemos a obtener un df con la descripcion de cada una de las combinaciones, 
#la descripcion que interesa es la de 'total_value'

descripcion = combinaciones.describe()['total_value']

#%%
"""

### solución al problema 1

### Analizaremos las rutas de importaciones para obtener las 10 mas demandadas
para importaciones.
"""

ruta_importaciones = synergy_dataframe[synergy_dataframe['direction'] == 'Imports'].copy()

combinaciones1 = ruta_importaciones.groupby(by=['origin', 'destination'])

descripcion = combinaciones1.describe()['total_value']


conteo_importaciones = descripcion['count']


# las 10 rutas de importación más demandadas
ruta_importaciones_sort = conteo_importaciones.sort_values(ascending=False).head(10)

#%%

### Analizaremos las rutas de importaciones para obtener las 10 mas demandadas
## para exportaciones.

ruta_exportaciones = synergy_dataframe[synergy_dataframe['direction'] == 'Exports'].copy()

combinaciones2 = ruta_exportaciones.groupby(by=['origin', 'destination'])

descripcion2 = combinaciones2.describe()['total_value']


conteo_exportaciones = descripcion2['count']


# las 10 rutas de importación más demandadas
ruta_exportaciones_sort = conteo_exportaciones.sort_values(ascending=False).head(10)

#%%

#Analizamos las rutas que transportan con mayor valor.

tabla_completa = descripcion.copy()
tabla_completa['multiplicacion'] = tabla_completa['count'] * tabla_completa['mean']

### se multiplican los vaalores de count y mean para que se obtenga el resultado 
### mas completo tomando en cuenta la cantidad de viajes e ingresos monetarios obtenidos

mean = descripcion['count']


total = tabla_completa['multiplicacion']


# Ordenaremos la serie mean de mayor a menor.
total_sort = total.sort_values(ascending=False).head(10)

#%%

"""
# solucion problema 2

# ruta de importaciones
"""

ruta_importaciones2 = synergy_dataframe[synergy_dataframe['direction'] == 'Imports'].copy()

combinacion_ruta2 = ruta_importaciones2.groupby(by=['transport_mode'])

descripcion_ruta2 = combinacion_ruta2.describe()['total_value']


tabla_completa2 = descripcion_ruta2.copy()

# Obtenemos el producto de count*mean, lo que nos da el total. 
tabla_completa2['multiplicacion'] = tabla_completa2['count'] * tabla_completa2['mean']

total_importaciones = tabla_completa2['multiplicacion']


# Ordenar la serie mean de mayor a menor.
total_importaciones_sort = total_importaciones.sort_values(ascending=False).head(10)

#%%


# ruta de exportaciones

ruta_exportaciones2 = synergy_dataframe[synergy_dataframe['direction'] == 'Exports'].copy()

combinacion_ruta3 = ruta_exportaciones2.groupby(by=['transport_mode'])

descripcion_ruta3 = combinacion_ruta3.describe()['total_value']


tabla_completa3 = descripcion_ruta3.copy()

# Obtenemos el producto de count*mean, lo que nos da el total. 
tabla_completa3['multiplicacion'] = tabla_completa3['count'] * tabla_completa3['mean']

total_exportaciones = tabla_completa3['multiplicacion']


# Ordenaremos la serie mean de mayor a menor.
total_exportaciones_sort = total_exportaciones.sort_values(ascending=False).head(10)



#%%

# Medios de transporte (Exportaciones e importaciones)

# Combinacion unica de 'product', 'transport_mode' y 'company_name'.
combinacion_conj = synergy_dataframe.groupby(by=['transport_mode'])


descripcion_conj = combinacion_conj.describe()['total_value']


tabla_completa_conj = descripcion_conj.copy()

# Obtenemos el producto de count*mean, lo que nos da el total. 
tabla_completa_conj['multiplicacion'] = tabla_completa_conj['count'] * tabla_completa_conj['mean']

total_conj = tabla_completa_conj['multiplicacion']


# Ordenaremos la serie mean de mayor a menor.
total_conj_sort = total_conj.sort_values(ascending=False).head(10)


#%%

# solución problema 3

exports = synergy_dataframe[synergy_dataframe['direction'] == 'Exports']
imports = synergy_dataframe[synergy_dataframe['direction'] == 'Imports']

def sol_3(df, p):
    pais_total_value = df.groupby('origin').sum()['total_value'].reset_index()
    total_value_for_percent = pais_total_value['total_value'].sum()
    pais_total_value['percent'] = 100 * pais_total_value['total_value']/ total_value_for_percent
    pais_total_value.sort_values(by='total_value', ascending=False, inplace=True)
    pais_total_value['cumsum'] = pais_total_value['percent'].cumsum()
    lista_pequena = pais_total_value[pais_total_value['cumsum'] < p]
    
    return lista_pequena

respuesta1 = sol_3(imports, 80)

respuesta2 = sol_3(exports, 80)

respuesta3 = sol_3(synergy_dataframe, 80)


