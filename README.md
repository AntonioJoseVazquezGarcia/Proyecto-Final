# **🌍 Análisis Exploratorio de Datos (EDA) y Dashboard de Clima y Geografía Global**

## **🎯 Objetivo del Proyecto**

Este proyecto se centra en un Análisis Exploratorio de Datos (EDA) para investigar la **relación entre las variables geográficas (Latitud, Longitud) y demográficas (Población, País) con las tendencias climáticas diarias (Temperatura y Precipitación)** de miles de ciudades a nivel global durante el año 2020\.

El objetivo final es construir un flujo de trabajo de ingeniería de datos robusto y generar un **Dashboard Operativo en Excel** que permita la exploración interactiva de los indicadores climáticos agregados por país, ciudad y mes.

## **🛠️ Estructura del Repositorio y Archivos**

Para mejorar la modularidad y la reproducibilidad, el proyecto se ha organizado en las siguientes carpetas, siguiendo las buenas prácticas en proyectos de Data Science:

| Carpeta/Archivo | Descripción |
| :---- | :---- |
| data\_raw/ | Contiene los dos datasets originales de Kaggle antes de cualquier manipulación: Weather all cities 2020.csv (registros climáticos) y World Cities Nearest Stations.csv (metadatos geográficos). |
| data\_processed/ | Almacena el dataset final (conjunto\_datos\_final\_transformado.csv) y el dataset agregado (data\_for\_dashboard.csv) listos para el análisis y la visualización. |
| src/ | Contiene los scripts de Python que definen el flujo de trabajo. |
| docs/ | Contiene la documentación del proyecto, incluyendo el informe detallado Proyecto Paso a Paso.docx. |
| dashboard/ | Contiene el panel de visualización interactivo en Excel (DashboardOperativo.08.xlsx). |
| README.md | Este archivo, que proporciona una visión general, instrucciones y conclusiones. |

## **⚙️ Instrucciones de Ejecución y Requisitos**

### **1\. Requisitos de Entorno**

Para ejecutar los scripts de Python en la carpeta src/, necesitarás tener instalado:

* **Python 3.x**  
* **Librerías:** pandas, numpy, matplotlib, seaborn (instalables vía pip install pandas numpy matplotlib seaborn)

### **2\. Flujo de Trabajo (Pipeline)**

El análisis se estructura en dos scripts principales que deben ejecutarse en orden:

| Orden | Archivo (src/) | Descripción del Proceso |
| :---- | :---- | :---- |
| **1\.** | ProyectoFinal.Paso01.01.py | **Ingeniería de Datos y Limpieza.** Carga los datos brutos, realiza la desambiguación de estaciones/ciudades (por distancia mínima), une los datasets con un *Left Join*, limpia nulos (eliminación de columnas \> 90% NaN), transforma unidades, crea variables de fecha y aplica imputación de valores faltantes mediante medias móviles por estación. |
| **2\.** | ProyectoFinal.Paso02.00.py | **Análisis y Agregación.** Realiza el Análisis Descriptivo (estadísticas, histogramas), el Análisis Estadístico (correlación Latitud-Temperatura, rankings de países) y genera el dataset final agregado por País, Ciudad y Mes (data\_for\_dashboard.csv) necesario para el dashboard. |

### **⚠️ Adaptación de Rutas**

**IMPORTANTE:** Los scripts originales utilizan rutas absolutas de disco local. Para reproducir el análisis, debes modificar las rutas dentro de ProyectoFinal.Paso01.01.py y ProyectoFinal.Paso02.00.py para que utilicen las **rutas relativas** del repositorio (por ejemplo, data\_raw/nombre\_archivo.csv).

## **📊 Resumen del Análisis y Hallazgos Clave**

El proyecto demostró un manejo profundo de datos complejos y arrojó varios *insights* interesantes sobre la climatología global en 2020:

### **Ingeniería y Limpieza de Datos**

* **Volumen y Complejidad:** El conjunto final supera ampliamente los requisitos mínimos, contando con más de **100.000 filas y 68 columnas**.  
* **Manejo de Duplicidades:** Se resolvió de manera efectiva el problema de la desambiguación de estaciones meteorológicas múltiples, seleccionando la estación con la distancia mínima a la ciudad correspondiente para asegurar una única clave de unión.  
* **Imputación Avanzada:** Se utilizó la técnica de la **media móvil centrada por estación** para imputar valores faltantes de temperatura y precipitación, aprovechando la estructura temporal de los datos.

### **Análisis Descriptivo y Estadístico**

* **Relación Latitud-Temperatura:** Se confirmó una clara **correlación negativa entre la Latitud y la Temperatura Media Diaria (TAVG)**, demostrando el patrón esperado de temperaturas más bajas a medida que las ciudades se alejan del ecuador (valores de latitud más extremos).  
* **Distribución de Datos:** Se empleó la escala logarítmica para analizar la variable population debido a su fuerte asimetría, permitiendo una interpretación más clara de la distribución demográfica de las ciudades en el dataset.  
* **Rankings Globales:** Se generaron rankings de países por temperatura media y precipitación total que sirven como base para la exploración en el dashboard.

### **Dashboard Operativo**

* El dashboard en Excel es **funcional y operativo**, utilizando Tablas Dinámicas y **Segmentación de Datos (Slicers)** para filtrar de forma simultánea los gráficos de temperatura media mensual y precipitación total mensual por **País**, **Ciudad** y **Mes**.  
* Esta interactividad permite al usuario explorar la estacionalidad y el comportamiento climático en cualquier ciudad seleccionada sin necesidad de manipular los datos o el código.

## **🚀 Próximos Pasos y Mejoras**

Como pasos futuros para elevar aún más la calidad del proyecto, se recomienda:

1. **Refuerzo Estadístico:** Incorporar un modelo sencillo de **Regresión Lineal** (TAVG \~ Latitud) para cuantificar la pendiente de la relación e incluir un intervalo de confianza.  
2. **Modularización del Código:** Encapsular los pasos del flujo (limpieza, imputación, agregación) en funciones dentro de Python para mejorar la reusabilidad y claridad del código.  
3. **Mejora del Dashboard:** Añadir tarjetas de indicadores (KPIs) con métricas clave (e.g., temperatura media anual de la ciudad seleccionada) y ajustar los formatos de número para una lectura más rápida y profesional.
