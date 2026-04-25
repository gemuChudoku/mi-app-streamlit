#  Análisis de Muertes por Disparos Policiales

##  Descripción
Este proyecto consiste en el análisis exploratorio de un dataset sobre incidentes de muertes causadas por disparos de la policía en Estados Unidos. A través de una aplicación interactiva desarrollada en Streamlit, se presentan diferentes visualizaciones que permiten identificar patrones, tendencias y relaciones entre variables como la edad, género, raza, nivel de amenaza, estado de huida y uso de cámaras corporales.

El objetivo principal es comprender el comportamiento de los datos mediante técnicas de visualización, sin establecer relaciones causales.

---

##  Dataset

- **Fuente**: FBI y Centers for Disease Control and Prevention (CDC)  
- **URL**: https://raw.githubusercontent.com/gemuChudoku/Archivos_csv/refs/heads/main/fatal-police-shootings-data.csv  
- **Descripción**:  
El dataset recopila información sobre incidentes de muertes por disparos policiales, incluyendo variables como edad, género, raza, ubicación, tipo de arma, nivel de amenaza, estado de huida y presencia de signos de enfermedad mental.

---

##  Hallazgos Principales

1. **Distribución por raza**: Se evidencia una mayor cantidad de casos en ciertos grupos raciales, mostrando una distribución desigual dentro del dataset.  

2. **Edad predominante**: La mayoría de los casos corresponde a adultos jóvenes, principalmente entre los 20 y 45 años.  

3. **Diferencia por género**: Los hombres representan una gran mayoría de los casos, evidenciando una afectación desproporcionada frente a otros géneros.  

4. **Comportamiento en los incidentes**: La mayoría de los casos ocurre sin intento de huida, lo que indica que estos eventos no están necesariamente asociados a persecuciones.  

5. **Distribución geográfica y temporal**: Algunos estados concentran mayor cantidad de casos, y se observan variaciones en el número de incidentes a lo largo del tiempo.

---

## 📊 Visualizaciones Implementadas

1. Gráfico de barras comparativo de casos por raza  
2. Distribución de edades (histograma y rangos)  
3. Relación entre variables (género vs nivel de amenaza, cámara corporal vs amenaza)  
4. Serie temporal del número de casos por año  
5. Mapa geográfico de casos por estado  
6. Gráficos de proporción (tipo de arma)  
7. Heatmap de correlaciones entre variables numéricas  

---

## ⚙️ Tecnologías Utilizadas

- **Framework**: Streamlit  
- **Lenguaje**: Python  
- **Bibliotecas**:  
  - pandas  
  - matplotlib  
  - seaborn  
  - plotly  

---

##  Instalación y Ejecución Local

###  Requisitos Previos

- Python 3.8 o superior  
- pip instalado  

###  Instrucciones

``bash
# Clonar repositorio
git clone https://github.com/gemuChudoku/mi-app-streamlit

# Entrar a la carpeta
cd repo

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
streamlit run app.py

##Autores
carlos losada
Harvey lozada
