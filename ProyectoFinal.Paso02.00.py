# El objetivo es extraer las primeras conclusiones clave sobre las tendencias climáticas y su relación con la ubicación geográfica.

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Configuración de visualización
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

# Cargar el DataFrame limpio y transformado
df_final = pd.read_csv(
    r'E:\Datos\Documents\Antonio José\PowerMBA\DataAnatytics\20.Proyecto Final\ProyectoFinal00\conjunto_datos_final_transformado.csv', 
    low_memory=False,
    sep=';',         # Le decimos que el separador de columnas es el punto y coma
    decimal=','      # Le decimos que el separador decimal es la coma (por seguridad)
)

# Asegurar que la columna 'Date' esté en formato datetime si no lo está
df_final['Date'] = pd.to_datetime(df_final['Date'])

print("✅ DataFrame Final cargado. Listo para el Análisis.")
print(f"Dimensiones: {df_final.shape}")

# Comenzamos con las estadísticas resumen para entender la escala de las variables clave.

print("\n--- Estadísticas Descriptivas del Clima y la Población ---")
# Enfocarse en las variables numéricas clave
descripcion = df_final[['TAVG', 'TMAX', 'TMIN', 'PRCP', 'population', 'lat', 'lng', 'Temp_Range']].describe().round(2)
print(descripcion)


'''Interpretación Clave de las Estadísticas:

Temperaturas (TAVG, TMAX, TMIN): Revisa si la media está en un rango lógico 
(debería estar cerca de 10-15 C para un promedio global anual). El valor mínimo y máximo indicará la amplitud 
climática cubierta.

Población (population): La media y el valor máximo muestran la concentración del análisis en áreas pobladas.
 El gran desvío estándar sugiere una amplia variabilidad (desde ciudades pequeñas hasta megalópolis).
 
Rango de Temperatura (Temp_Range): 
La media indica la oscilación térmica diaria promedio en el conjunto de datos.'''

#Visualizamos la forma de las variables más importantes: temperatura y población.

# 🌡️ Distribución de la Temperatura Media (TAVG)
plt.figure(figsize=(12, 5))
sns.histplot(df_final['TAVG'], bins=50, kde=True, color='skyblue')
plt.title('Distribución de la Temperatura Media Diaria (TAVG) en 2020')
plt.xlabel('Temperatura Media (°C)')
plt.ylabel('Frecuencia de Observaciones')
plt.show()

# 🧍 Distribución de la Población (usando logaritmo para manejar la asimetría)
plt.figure(figsize=(12, 5))
# Se usa logaritmo debido a la asimetría extrema de la población
sns.histplot(np.log1p(df_final['population']), bins=50, kde=True, color='salmon')
plt.title('Distribución de la Población (Escala Logarítmica)')
plt.xlabel('Población (log(1+Población))')
plt.ylabel('Frecuencia de Ciudades')
plt.show()

'''Análisis Estadístico: Correlación Geografía vs. Clima
El principal análisis que nos permite la unión de estos datos es la correlación entre la ubicación geográfica
 y la temperatura, confirmando el efecto climático estacional y latitudinal.'''

print("\n--- Correlación entre Latitud y Temperatura Media (General) ---")

# Calculamos la correlación de Pearson
correlacion_lat_temp = df_final['lat'].corr(df_final['TAVG'])
print(f"Coeficiente de Correlación (Latitud vs. TAVG): {correlacion_lat_temp:.4f}")

# Visualización: Gráfico de Dispersión
plt.figure(figsize=(10, 6))
sns.scatterplot(x='lat', y='TAVG', data=df_final, alpha=0.1, color='blue')
plt.title('Dispersión de la Latitud vs. Temperatura Media (2020)')
plt.xlabel('Latitud (°)')
plt.ylabel('Temperatura Media (°C)')
plt.show()

print("\nLa correlación cercana a cero o la forma parabólica en el gráfico indica que la relación cambia según la estación del año o si se está en el hemisferio Norte o Sur.")

print("\n--- Top 10 Países por Temperatura Media y Precipitación ---")

# Agrupar por país y calcular las medias
df_analisis_pais = df_final.groupby('country').agg(
    Temperatura_Media=('TAVG', 'mean'),
    Precipitacion_Media=('PRCP', 'mean'),
    Total_Registros=('ID', 'count')
).reset_index()

# Filtrar para considerar solo países con un número significativo de registros
df_analisis_pais = df_analisis_pais[df_analisis_pais['Total_Registros'] >= 1000]

# 🌡️ Top 10 Países más cálidos
top_temp = df_analisis_pais.sort_values(by='Temperatura_Media', ascending=False).head(10)
print("\nTop 10 Países más Cálidos (Media Anual):")
print(top_temp[['country', 'Temperatura_Media']].to_string(index=False))

# 🌧️ Top 10 Países con mayor Precipitación (Media Diaria)
top_prcp = df_analisis_pais.sort_values(by='Precipitacion_Media', ascending=False).head(10)
print("\nTop 10 Países con Mayor Precipitación (Media Diaria):")
print(top_prcp[['country', 'Precipitacion_Media']].to_string(index=False))

# Preparación de la tabla final para el Dashboard
df_dashboard = df_final.groupby(['country', 'city', 'Month']).agg(
    Temperatura_Media_Mensual=('TAVG', 'mean'),
    Precipitacion_Total_Mensual=('PRCP', 'sum'),
    Poblacion_Estimada=('population', 'first'), # La población es constante, tomamos la primera
    Latitud=('lat', 'first'),
    Longitud=('lng', 'first')
).reset_index()

# Crear una columna de mes legible
meses_map = {1: 'Ene', 2: 'Feb', 3: 'Mar', 4: 'Abr', 5: 'May', 6: 'Jun', 
             7: 'Jul', 8: 'Ago', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dic'}
df_dashboard['Month_Name'] = df_dashboard['Month'].map(meses_map)

# Exportar para su uso en Power BI / Excel con separador decimal ',' y separador de campo ';'
# Esto es necesario para la correcta lectura en configuraciones regionales europeas/españolas.
# Importante: Usamos sep=';' como delimitador de campos y decimal=',' como separador decimal
df_dashboard.to_csv('data_for_dashboard.csv', index=False, sep=';', decimal=',')

print("\n--- Archivo para Dashboard Exportado: 'data_for_dashboard.csv' ---")
print("Contiene datos agregados por País, Ciudad y Mes, perfecto para filtros y visualizaciones interactivas.")



