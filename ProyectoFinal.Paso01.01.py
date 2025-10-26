import pandas as pd
import numpy as np

# --- 1. Carga de los conjuntos de datos originales ---
df_ciudades = pd.read_csv(r'E:\Datos\Documents\Antonio José\PowerMBA\DataAnatytics\20.Proyecto Final\ProyectoFinal00\World Cities Nearest Stations.csv', low_memory=False)
df_clima = pd.read_csv(r'E:\Datos\Documents\Antonio José\PowerMBA\DataAnatytics\20.Proyecto Final\ProyectoFinal00\Weather all cities 2020.csv', low_memory=False)

print("✅ Archivos CSV cargados con éxito.")

# --- 2. Preparación y Deduplicación del Dataset de Ciudades ---
df_ciudades = df_ciudades.rename(columns={'Closest Station ID': 'ID'})
idx = df_ciudades.groupby('ID')['Closest Station Distance'].idxmin()
df_ciudades_unicas = df_ciudades.loc[idx]
print(f"Número de estaciones únicas después de desambiguación: {len(df_ciudades_unicas)}")

# --- 3. Filtrado y Unión de los DataFrames (Left Join) ---
columnas_ciudades = [
    'ID', 'city', 'country', 'iso3', 'lat', 'lng', 'population', 'Closest Station Distance'
]
df_ciudades_filtrado = df_ciudades_unicas[columnas_ciudades]

# Realizar la unión con el DataFrame de clima (CREACIÓN de df_final)
df_final = pd.merge(
    left=df_clima, 
    right=df_ciudades_filtrado, 
    on='ID', 
    how='left'
)
print(f"\n✅ Unión de datos completada (Left Merge).")

# --- 4. Transformación y Limpieza profunda de los datos ---

# 4.1 Eliminación de Columnas con Demasiados NaN
umbral_nan = len(df_final) * 0.9
columnas_a_eliminar = df_final.columns[df_final.isnull().sum() > umbral_nan]
df_final = df_final.drop(columns=columnas_a_eliminar)
print(f"Columnas eliminadas por más del 90% de NaN: {list(columnas_a_eliminar)}")

# 4.2 Conversión de Unidades de Clima (SOLUCIÓN A VALORES INCOHERENTES)
# Las unidades están en décimas de Celsius/milímetro, hay que dividirlas por 10.
columnas_clima_a_convertir = ['TAVG', 'TMAX', 'TMIN', 'TOBS', 'PRCP'] 
for col in columnas_clima_a_convertir:
    if col in df_final.columns:
        df_final[col] = df_final[col] / 10.0
print("✅ Conversión de unidades climáticas (Temperatura y Precipitación) completada.")

# 4.3 Conversión y Extracción de Fechas
df_final['Date'] = pd.to_datetime(df_final['Date'].astype(str), format='%Y%m%d', errors='coerce')
df_final['Year'] = df_final['Date'].dt.year
df_final['Month'] = df_final['Date'].dt.month
df_final['DayOfWeek'] = df_final['Date'].dt.day_name()
df_final['DayOfYear'] = df_final['Date'].dt.dayofyear
df_final['Temp_Range'] = df_final['TMAX'] - df_final['TMIN']

# 4.4 Limpieza y Conversión de Variables de Geografía/Demografía
df_final['city'] = df_final['city'].str.title()
df_final['country'] = df_final['country'].str.title()
df_final['population'] = pd.to_numeric(df_final['population'], errors='coerce')

# 4.5 Imputación de NaN (Media Móvil)
df_final = df_final.sort_values(by=['ID', 'Date'])
for col in ['TAVG', 'TMAX', 'TMIN', 'PRCP']:
    if col in df_final.columns:
        df_final[col + '_Impute'] = df_final.groupby('ID')[col].transform(
            lambda x: x.fillna(x.rolling(7, min_periods=1, center=True).mean())
        )
        df_final[col] = df_final[col + '_Impute']
        df_final = df_final.drop(columns=[col + '_Impute'])

# Limpiar filas finales con NaN en columnas clave
df_final = df_final.dropna(subset=['TAVG', 'ID'])

# --- 5. Verificación y Guardado ---
print(f"\n--- Verificación de Requisitos Finales ---")
print(f"Filas Totales: {len(df_final)} (Mínimo: 50,000)")
print(f"Columnas Totales: {len(df_final.columns)} (Mínimo: 20)")

# **VERIFICACIÓN DEL MES** (¡Clave!)
conteo_meses = df_final['Month'].value_counts().sort_index()
print("\n--- Distribución Mensual de Datos ---")
print(conteo_meses)
if len(conteo_meses) < 12:
    print("⚠️ ADVERTENCIA: Solo hay datos para algunos meses. Confirma que usaste el archivo de clima completo.")

df_final.to_csv('conjunto_datos_final_transformado.csv', index=False, sep=';', decimal=',')
print("\n✅ DataFrame final guardado como 'conjunto_datos_final_transformado.csv'.")