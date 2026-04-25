import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
# -------------------------------
# CONFIGURACIÓN GENERAL
# -------------------------------
st.set_page_config(page_title="Análisis IA", layout="wide")

# -------------------------------
# CARGA DE DATOS
# -------------------------------
 # 🔹 Cargar datos
@st.cache_data
def load_data():
    df = pd.read_csv(
        "https://raw.githubusercontent.com/gemuChudoku/Archivos_csv/refs/heads/main/fatal-police-shootings-data.csv"
    )

    race_map = {
        "W": "Blanco",
        "B": "Negro",
        "A": "Asiatico",
        "N": "Nativo Americano",
        "H": "Hispanico",
        "O": "Otros"
    }

    df["race"] = df["race"].map(race_map).fillna("Desconocido")

    df["gender"] = df["gender"].map({
        "M": "Hombre",
        "F": "Mujer"
    })

    df["body_camera"] = df["body_camera"].map({
        True: "Si",
        False: "No"
    })

    df["armed"] = df["armed"].map({
        "gun": "Arma de fuego",
        "vehicle": "Vehiculo",
        "undertermined": "No determinado",
        "toy weapon": "Arma de juguete",
        "unarmed": "Desarmado",
        "knife": "Cuchillo"
    })


    df["flee"] = df["flee"].map({
        "Not fleeing": "No huyen",
        "Car": "Vehiculo",
        "Foot": "A pie",
        "Other": "Otro"
    }).fillna("Desconocido")

    df["threat_level"] = df["threat_level"].map({
        "attack": "Atacaron",
        "other": "Otro",
        "undetermined": "Sin determinar"
    })

    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year

    df = df[df["year"] < 2020]

    return df


df = load_data()

# -------------------------------
# SIDEBAR (NAVEGACIÓN)
# -------------------------------
st.sidebar.title("📊 Navegación")

section = st.sidebar.selectbox(
    "Ir a:",
    [
        "Inicio",
        "Casos por raza", 
        "numero de casos por año",
        "Distribución de edades",
        "Amenazas",
        "casos segun huida",
        "tipo de arma",
        "Genero",
        "casos por estado",
        "Conclusiones"
    ]
)

# -------------------------------
# SECCIÓN: INICIO
# -------------------------------
if section == "Inicio":

    st.title("Introducción")

    st.markdown("""
    El presente análisis se basa en un dataset que recopila información sobre incidentes de muertes causadas por disparos de la policía. Este conjunto de datos es proporcionado por el FBI y los Centros para el Control y la Prevención de Enfermedades (CDC), entidades encargadas de registrar y documentar este tipo de eventos.

    El dataset contiene un total de 5416 registros y 14 variables, entre las que se incluyen características relevantes como la edad, género, raza, ciudad y estado donde ocurrió el incidente, así como información relacionada con el nivel de amenaza percibida, el tipo de arma involucrada, la presencia de signos de enfermedad mental, el estado de huida y el uso de cámaras corporales.

    A partir de esta información, es posible realizar un análisis exploratorio de datos que permita identificar patrones, tendencias y relaciones entre las variables.
    """)

    # 🔹 Mostrar datos
    st.subheader("Vista previa del dataset")
    st.dataframe(df.head())

    # 🔹 Info general
    st.subheader("Información general")
    st.write(df.describe())

    # 🔹 Valores nulos
    st.subheader("Valores nulos")
    st.write(df.isnull().sum())


    st.title("Análisis de Dataset: Fatal Shootings by Police")

    st.subheader("Hallazgos Insights y Visualizaciones")

    st.subheader("1. Predominio de casos en ciertos grupos raciales")
    st.write(""" Insight: 
    Se observa que algunos grupos raciales concentran una mayor cantidad de casos dentro del dataset, lo que evidencia una distribución desigual en la frecuencia de incidentes.
    
    Visualización recomendada:  
    Gráfico de barras (countplot)
             
    Justificación:
    Este tipo de gráfico permite comparar fácilmente la cantidad de casos entre diferentes categorías, facilitando la identificación de los grupos con mayor frecuencia.
    """)
    

    st.subheader("2. Concentración de edades en adultos jóvenes")
    st.write(""" Insight:
    La mayoría de los casos se concentra en personas entre aproximadamente 20 y 45 años, con una media cercana a los 37 años, lo que indica que los incidentes ocurren principalmente en población adulta joven.

    Visualización recomendada:
    Histograma o gráfico por rangos de edad

    Justificación:
    Permite observar la distribución de una variable numérica y detectar los rangos de edad más frecuentes dentro del dataset.
    """)
    
    st.subheader("3. Predominancia del nivel de amenaza ataque")
    st.write(""" Insight:
    El nivel de amenaza clasificado como ataque aparece con mayor frecuencia en comparación con otras categorías como otros o sin determinar.

    Visualización recomendada:
    Gráfico de barras (countplot)

    Justificación:
    Facilita la comparación directa entre categorías discretas y permite identificar cuál es la más representativa.
     """)
    
    st.subheader("4. La mayoría de los incidentes ocurren sin intento de huida")
    st.write(""" Insight:  
    Una proporción significativa de los casos corresponde a situaciones donde el individuo no estaba huyendo, en comparación con aquellos que huían a pie o en vehículo.

    Visualización recomendada:  
    Gráfico de barras (countplot)

    Justificación:  
    Permite analizar la frecuencia de cada categoría dentro de la variable `flee`, facilitando la interpretación del comportamiento en los incidentes.
     """)
    
    st.subheader("5. Presencia minoritaria de signos de enfermedad mental")
    st.write(""" Insight:
    Aunque existen casos donde se identifican signos de enfermedad mental, estos representan una proporción menor frente a los casos donde no se reportan dichos signos.

    Visualización recomendada:
    Gráfico de barras (countplot)

    Justificación:
    Permite comparar claramente la proporción entre dos categorías (presencia o ausencia de signos).
    """)
    
    st.subheader("6. Variación temporal en el número de casos")
    st.write(""" Insight:
    El número de incidentes presenta variaciones a lo largo de los años, lo que permite identificar tendencias en el tiempo.

    Visualización recomendada:  
    Gráfico de líneas o barras por año

    Justificación: 
    Este tipo de gráfico es el más adecuado para representar cambios y evolución temporal en los datos.
    """)
#------------------------------------
# casos por raza
#----------------------------------


elif section == "Casos por raza":

    st.title(" Número de casos por raza")

    # 🔹 Filtro (multiselección)
    selected_races = st.multiselect(
        "Filtrar por raza:",
        options=df["race"].dropna().unique(),
        default=df["race"].dropna().unique()
    )

    # Filtrar dataset
    df_filtered = df[df["race"].isin(selected_races)]

    # Agrupar datos
    race_counts = df_filtered["race"].value_counts().reset_index()
    race_counts.columns = ["race", "cases"]

    # 🔹 Gráfica interactiva
    fig = px.bar(
        race_counts,
        x="race",
        y="cases",
        color="race",
        title="Número de casos por raza",
        labels={"race": "Raza", "cases": "Cantidad de casos"}
    )

    # Hover más claro
    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>Casos: %{y}<extra></extra>"
    )

    st.plotly_chart(fig, use_container_width=True)

    # 🔹 Interpretación
    st.markdown("""
    ### Interpretación

    La gráfica muestra la distribución de los casos según la variable de raza. Se observa que el grupo "Blanco" presenta la mayor cantidad de registros dentro del dataset, seguido por los grupos "Negro" e "Hispánico".  

    Por otro lado, los grupos "Asiático", "Nativo Americano" y "Otros" presentan una frecuencia considerablemente menor.  

    Esta diferencia evidencia una distribución desigual en la representación de los casos entre los distintos grupos raciales dentro del conjunto de datos.
    """)
    #-------------------------------------------
    #impacto general
    #-------------------------------------------


elif section == "Distribución de edades":
    st.title(" Distribución de edades")

    st.subheader("📊 Distribución por rangos de edad")

    bins = list(range(0, int(df["age"].max()) + 10, 10))
    labels = [f"{i}-{i+9}" for i in bins[:-1]]

    df_age = df.copy()

    df_age["age_range"] = pd.cut(
        df_age["age"],
        bins=bins,
        labels=labels,
        right=False
    )

    age_counts = df_age["age_range"].value_counts().sort_index().reset_index()
    age_counts.columns = ["age_range", "cases"]

    fig = px.bar(
        age_counts,
        x="age_range",
        y="cases",
        title="Distribución por rangos de edad"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("interpretación")
    st.write("""La distribución de edades presenta una concentración notable en el rango de aproximadamente 20 a 45 años, lo que indica que la mayoría de los casos corresponde a adultos jóvenes. 

La curva de densidad muestra una ligera asimetría hacia la derecha, evidenciando que existen casos en edades más altas, aunque con menor frecuencia. Asimismo, se identifican algunos valores extremos en edades avanzadas, pero estos no representan una proporción significativa dentro del total.""")
#-----------------------------------------------------------
# Amenazas
#-----------------------------------------------------------



elif section == "Amenazas":

    st.title("📊 Uso de cámara corporal vs nivel de amenaza")

    # 🔹 Filtros
    col1, col2 = st.columns(2)

    with col1:
        selected_camera = st.multiselect(
            "Filtrar por uso de cámara:",
            options=df["body_camera"].dropna().unique(),
            default=df["body_camera"].dropna().unique()
        )

    with col2:
        selected_threat = st.multiselect(
            "Filtrar por nivel de amenaza:",
            options=df["threat_level"].dropna().unique(),
            default=df["threat_level"].dropna().unique()
        )

    # Filtrar datos
    df_filtered = df[
        (df["body_camera"].isin(selected_camera)) &
        (df["threat_level"].isin(selected_threat))
    ]

    # Agrupar
    grouped = df_filtered.groupby(["body_camera", "threat_level"]).size().reset_index(name="cases")

    # 🔹 Gráfica interactiva
    fig = px.bar(
        grouped,
        x="body_camera",
        y="cases",
        color="threat_level",
        barmode="group",
        title="Uso de cámara corporal vs nivel de amenaza",
        labels={
            "body_camera": "Uso de cámara corporal",
            "cases": "Cantidad de casos",
            "threat_level": "Nivel de amenaza"
        }
    )

    # Hover personalizado
    fig.update_traces(
        hovertemplate="<b>Cámara:</b> %{x}<br><b>Amenaza:</b> %{legendgroup}<br>Casos: %{y}<extra></extra>"
    )

    st.plotly_chart(fig, use_container_width=True)

    # 🔹 Interpretación
    st.markdown("""
    ### Interpretación

    La visualización muestra la relación entre el uso de cámaras corporales y el nivel de amenaza en los incidentes. Se observa que la mayoría de los casos ocurrieron sin el uso de cámara corporal, independientemente del nivel de amenaza.

    El nivel de amenaza **"Atacaron"** es el más frecuente en ambos grupos (con y sin cámara), seguido por **"Otro"** y finalmente **"Sin determinar"**.  

    Además, se evidencia que los casos donde sí se utilizó cámara corporal son considerablemente menores en comparación con aquellos donde no se utilizó.

    Esto sugiere que, dentro del dataset, el uso de cámaras corporales no es predominante y que la distribución del nivel de amenaza se mantiene relativamente consistente en ambos escenarios.
    """)

    st.subheader("📊 Signos de enfermedad mental vs nivel de amenaza")

    # 🔹 Filtros
    col1, col2 = st.columns(2)

    with col1:
        selected_mental = st.multiselect(
            "Filtrar por signos de enfermedad mental:",
            options=df["signs_of_mental_illness"].dropna().unique(),
            default=df["signs_of_mental_illness"].dropna().unique()
        )

    with col2:
        selected_threat = st.multiselect(
            "Filtrar por nivel de amenaza 2:",
            options=df["threat_level"].dropna().unique(),
            default=df["threat_level"].dropna().unique()
        )

    # 🔹 Filtrar datos
    df_filtered_mental = df[
        (df["signs_of_mental_illness"].isin(selected_mental)) &
        (df["threat_level"].isin(selected_threat))
    ]

    # 🔹 Agrupar
    grouped_mental = df_filtered_mental.groupby(
        ["signs_of_mental_illness", "threat_level"]
    ).size().reset_index(name="cases")

    # 🔹 Gráfica
    fig_mental = px.bar(
        grouped_mental,
        x="signs_of_mental_illness",
        y="cases",
        color="threat_level",
        barmode="group",
        title="Signos de enfermedad mental vs nivel de amenaza",
        labels={
            "signs_of_mental_illness": "Presenta signos",
            "cases": "Cantidad de casos",
            "threat_level": "Nivel de amenaza"
        }
    )

    # Hover personalizado
    fig_mental.update_traces(
        hovertemplate="<b>Signos:</b> %{x}<br><b>Amenaza:</b> %{legendgroup}<br>Casos: %{y}<extra></extra>"
    )

    st.plotly_chart(fig_mental, use_container_width=True)

#----------------------------------------------
#casos segun huida
#--------------------------------------------

elif section == "casos segun huida":
    st.title("📊 Número de casos según estado de huida")

    # 🔹 Filtro
    selected_flee = st.multiselect(
        "Filtrar por estado de huida:",
        options=df["flee"].dropna().unique(),
        default=df["flee"].dropna().unique(),
        key="flee_filter"
    )

    # Filtrar datos
    df_filtered_flee = df[df["flee"].isin(selected_flee)]

    # Agrupar
    flee_counts = df_filtered_flee["flee"].value_counts().reset_index()
    flee_counts.columns = ["flee", "cases"]

    # 🔹 Gráfica interactiva
    fig_flee = px.bar(
        flee_counts,
        x="flee",
        y="cases",
        color="flee",
        title="Número de casos según estado de huida",
        labels={
            "flee": "Estado de huida",
            "cases": "Cantidad de casos"
        }
    )

    # Hover personalizado
    fig_flee.update_traces(
        hovertemplate="<b>%{x}</b><br>Casos: %{y}<extra></extra>"
    )

    st.plotly_chart(fig_flee, use_container_width=True)


elif section == "Rendimiento académico":
    st.title("📚 Uso de IA vs rendimiento académico")

    fig = px.box(
        df,
        x="Affects_Academic_Performance",
        y="Avg_Daily_Usage_Hours",
        color="Affects_Academic_Performance",
        color_discrete_map={
            "Yes": "#E24B4A",
            "No": "#4A90E2"
        },
        title="Uso diario de IA vs impacto en el rendimiento académico"
    )

    # Hover personalizado
    fig.update_traces(
        hovertemplate="Categoría: %{x}<br>Horas de uso: %{y:.2f}"
    )

    # Quitar leyenda si quieres (opcional)
    fig.update_layout(showlegend=False)

    # Etiquetas
    fig.update_layout(
        xaxis_title="¿Afecta el rendimiento académico?",
        yaxis_title="Horas promedio de uso diario"
    )

    st.plotly_chart(fig)

    st.write("""###  Interpretación: Uso de IA/Redes sociales vs Rendimiento Académico

Se observa que los estudiantes que indican que **sí existe un impacto en su rendimiento académico** presentan, en general, un **mayor número de horas de uso diario**, con una mediana cercana a las 6 horas. En contraste, aquellos que consideran que **no hay impacto** muestran un uso más moderado, con una mediana aproximada de entre 3 y 4 horas diarias.

Además, el grupo que percibe un impacto negativo presenta una mayor dispersión en los datos, lo que indica variabilidad en los hábitos de uso. Por otro lado, en el grupo que no percibe impacto, aunque el uso es menor, se observan algunos valores atípicos (outliers) con altos niveles de uso, lo que sugiere que no todos los casos siguen la tendencia general.

Estos resultados sugieren una posible relación entre el **uso intensivo de herramientas de inteligencia artificial** y la percepción de afectación en el rendimiento académico. Sin embargo, no se puede afirmar causalidad directa, ya que pueden existir otros factores involucrados.

En conjunto, esta visualización aporta evidencia relevante para el análisis, indicando que un mayor tiempo de uso podría estar asociado con efectos percibidos en el desempeño académico.""")

#-----------------------------------------------
# numero de casos por año
#------------------------------------------------


elif section == "numero de casos por año":
    st.title("📊 Número de casos por año")

    min_year = int(df["year"].min())
    max_year = int(df["year"].max())

    year_range = st.slider(
        "Selecciona rango de años:",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
        key="year_slider"
    )

    # Filtrar datos
    df_filtered_year = df[
        (df["year"] >= year_range[0]) &
        (df["year"] <= year_range[1])
    ]

    # Agrupar
    cases_per_year = df_filtered_year.groupby("year").size().reset_index(name="cases")

    # 🔹 Gráfica interactiva (línea + puntos)
    fig_year = px.line(
        cases_per_year,
        x="year",
        y="cases",
        markers=True,
        title="Número de casos por año",
        labels={"year": "Año", "cases": "Cantidad de casos"}
    )

    # Hover personalizado
    fig_year.update_traces(
        hovertemplate="Año: %{x}<br>Casos: %{y}<extra></extra>"
    )

    st.plotly_chart(fig_year, use_container_width=True)

    st.subheader("Interpretación")
    st.write("""Durante el período 2015–2019, el número de muertes por disparos policiales se mantuvo en niveles muy similares cada año, oscilando alrededor de las 990 muertes anuales. Esta estabilidad sugiere que no se produjeron cambios estructurales relevantes en las políticas o prácticas policiales que lograran impactar el fenómeno, el cual parece haberse consolidado como un problema crónico y sostenido en el período analizado.
    """)
#-----------------------------------------------
# tipo de arma
#------------------------------------------------


elif section == "tipo de arma":
    st.title("📊 Edad según tipo de arma")

    # 🔹 Filtro: tipos de arma (top para no saturar)
    top_armed = df["armed"].value_counts().nlargest(6).index

    selected_armed = st.multiselect(
        "Filtrar tipo de arma:",
        options=top_armed,
        default=top_armed,
        key="armed_filter"
    )

    # Filtrar datos
    df_filtered_armed = df[df["armed"].isin(selected_armed)]

    # 🔹 Boxplot interactivo
    fig_box = px.box(
        df_filtered_armed,
        x="armed",
        y="age",
        color="armed",
        title="Edad según tipo de arma",
        labels={"armed": "Tipo de arma", "age": "Edad"}
    )

    fig_box.update_traces(
        hovertemplate="Arma: %{x}<br>Edad: %{y}<extra></extra>"
    )

    st.plotly_chart(fig_box, use_container_width=True)

    # 🔹 Interpretación
    st.markdown("""
    ### Interpretación

    Independientemente del tipo de arma involucrada en el incidente, las víctimas corresponden en su mayoría a adultos jóvenes de entre 30 y 40 años.  

    La distribución de edades es relativamente homogénea entre las distintas categorías, lo que indica que la edad no actúa como un factor diferenciador relevante según el tipo de arma.  

    Sin embargo, los casos asociados a armas de fuego presentan una mayor dispersión, incluyendo víctimas de edades más elevadas.
    """)


    st.subheader("📊 Proporción de tipo de arma")

    # 🔹 Filtro (top 6)
    top_armed_counts = df["armed"].value_counts().nlargest(6).reset_index()
    top_armed_counts.columns = ["armed", "cases"]

    fig_pie = px.pie(
        top_armed_counts,
        names="armed",
        values="cases",
        title="Proporción de tipo de arma"
    )

    fig_pie.update_traces(
        hovertemplate="<b>%{label}</b><br>Casos: %{value}<br>Porcentaje: %{percent}<extra></extra>"
    )

    st.plotly_chart(fig_pie, use_container_width=True)

    # 🔹 Interpretación
    st.markdown("""
    ### Interpretación

    La mayoría de los casos involucra personas que portaban armas de fuego, siendo esta categoría la de mayor proporción dentro del dataset.  

    En segundo lugar se encuentran otros tipos de armas como cuchillos, con una participación considerablemente menor.  

    Adicionalmente, se identifican casos en los que las personas estaban desarmadas o portaban armas de juguete, lo que representa una fracción significativa y plantea cuestionamientos sobre la percepción del nivel de amenaza en estos incidentes.
    """)

#------------------------------------------------
#sueño
#-----------------------------------------------


elif section == "Sueño":
    st.title("😴 Uso de IA vs Horas de sueño")

    fig = px.scatter(
        df,
        x="Avg_Daily_Usage_Hours",
        y="Sleep_Hours_Per_Night",
        opacity=0.6,
        trendline="ols",  # 👈 línea de regresión
        title="Relación entre uso de IA y horas de sueño"
    )

    # Personalizar colores (puntos y línea)
    fig.update_traces(
        marker=dict(color="#7F77DD"),
        hovertemplate=(
            "Horas de uso: %{x}<br>"
            "Horas de sueño: %{y}"
        )
    )

    # Cambiar estilo de la línea de tendencia
    fig.data[1].line.color = "#E24B4A"
    fig.data[1].line.dash = "dash"

    # Etiquetas
    fig.update_layout(
        xaxis_title="Horas promedio de uso diario",
        yaxis_title="Horas de sueño por noche"
    )

    st.plotly_chart(fig)
    st.write("""### Interpretación: Uso de IA vs Horas de Sueño

La visualización muestra una relación negativa entre el tiempo de uso diario de herramientas de inteligencia artificial y las horas de sueño de los estudiantes.

La línea de tendencia descendente indica que, a medida que aumentan las horas de uso, las horas de sueño tienden a disminuir. Esto sugiere que un mayor uso de estas tecnologías podría estar asociado con una reducción en el tiempo de descanso nocturno.

Aunque los datos presentan cierta dispersión, la tendencia general es clara y consistente, evidenciando que los estudiantes con un uso más intensivo tienden a dormir menos horas en promedio.
""")

#--------------------------
#heat map
#--------------------------


elif section == "Genero":
    st.title("📊 Distribución de casos por género")


    # 🔹 Filtro (por si quieres ocultar alguno)
    selected_gender = st.multiselect(
        "Filtrar por género:",
        options=df["gender"].dropna().unique(),
        default=df["gender"].dropna().unique(),
        key="gender_filter"
    )

    df_filtered_gender = df[df["gender"].isin(selected_gender)]

    # Agrupar
    gender_counts = df_filtered_gender["gender"].value_counts().reset_index()
    gender_counts.columns = ["gender", "cases"]

    # 🔹 Gráfica
    fig_gender = px.bar(
        gender_counts,
        x="gender",
        y="cases",
        color="gender",
        title="Distribución de casos por género",
        labels={"gender": "Género", "cases": "Cantidad de casos"}
    )

    fig_gender.update_traces(
        hovertemplate="<b>%{x}</b><br>Casos: %{y}<extra></extra>"
    )

    st.plotly_chart(fig_gender, use_container_width=True)

    # 🔹 Interpretación
    st.markdown("""
    ### Interpretación

    La diferencia entre géneros es muy marcada: los hombres representan la gran mayoría de los casos dentro del dataset, mientras que la cantidad correspondiente a mujeres es considerablemente menor.

    Esto indica que los incidentes analizados afectan de manera desproporcionada a la población masculina, evidenciando una distribución altamente desigual entre los géneros.
    """)

    st.subheader("📊 Género vs nivel de amenaza")

    # 🔹 Filtros
    col1, col2 = st.columns(2)

    with col1:
        selected_gender2 = st.multiselect(
            "Filtrar género:",
            options=df["gender"].dropna().unique(),
            default=df["gender"].dropna().unique(),
            key="gender_filter_2"
        )

    with col2:
        selected_threat_gender = st.multiselect(
            "Filtrar nivel de amenaza:",
            options=df["threat_level"].dropna().unique(),
            default=df["threat_level"].dropna().unique(),
            key="threat_filter_gender"
        )

    # Filtrar
    df_filtered_gt = df[
        (df["gender"].isin(selected_gender2)) &
        (df["threat_level"].isin(selected_threat_gender))
    ]

    # Agrupar
    grouped_gt = df_filtered_gt.groupby(
        ["gender", "threat_level"]
    ).size().reset_index(name="cases")

    # 🔹 Gráfica
    fig_gt = px.bar(
        grouped_gt,
        x="gender",
        y="cases",
        color="threat_level",
        barmode="group",
        title="Género vs nivel de amenaza",
        labels={
            "gender": "Género",
            "cases": "Cantidad de casos",
            "threat_level": "Nivel de amenaza"
        }
    )

    fig_gt.update_traces(
        hovertemplate="<b>Género:</b> %{x}<br><b>Amenaza:</b> %{legendgroup}<br>Casos: %{y}<extra></extra>"
    )

    st.plotly_chart(fig_gt, use_container_width=True)

    # 🔹 Interpretación
    st.markdown("""
    ### Interpretación

    Al analizar la relación entre género y nivel de amenaza, se observa que en ambos géneros la categoría más frecuente corresponde a situaciones clasificadas como "Atacaron".

    En el caso de los hombres, también se presenta una cantidad considerable de casos en la categoría "Otro", lo que indica que una proporción relevante de los incidentes no se clasifica directamente como una amenaza activa.

    Por su parte, la categoría "Sin determinar" tiene una presencia mínima en ambos géneros, lo que sugiere que la mayoría de los casos cuenta con algún tipo de clasificación definida.
    """)


elif section == "casos por estado":
    st.title("🗺️ Número de casos por estado")

    # 🔹 Filtro: rango de años (reutilizamos columna year)
    min_year = int(df["year"].min())
    max_year = int(df["year"].max())

    year_range_map = st.slider(
        "Filtrar por rango de años:",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
        key="year_map"
    )

    # Filtrar dataset
    df_filtered_map = df[
        (df["year"] >= year_range_map[0]) &
        (df["year"] <= year_range_map[1])
    ]

    # 🔹 Contar casos por estado
    cases_by_state = df_filtered_map["state"].value_counts().reset_index()
    cases_by_state.columns = ["state", "cases"]

    # 🔹 Crear mapa
    fig_map = px.choropleth(
        cases_by_state,
        locations="state",
        locationmode="USA-states",
        color="cases",
        scope="usa",
        color_continuous_scale="Reds",
        title="Número de casos por estado"
    )

    # Hover personalizado
    fig_map.update_traces(
        hovertemplate="<b>Estado:</b> %{location}<br>Casos: %{z}<extra></extra>"
    )

    st.plotly_chart(fig_map, use_container_width=True)
    st.markdown("""
### Interpretación

El mapa evidencia una distribución geográfica desigual de los incidentes a lo largo del territorio de Estados Unidos.

Se observa que algunos estados concentran una mayor cantidad de casos, destacándose aquellos con mayor densidad poblacional y actividad urbana. En particular, estados como California, Texas y Florida presentan una mayor intensidad en la coloración, lo que indica una mayor frecuencia de incidentes.

Por otro lado, varios estados presentan una menor cantidad de casos, reflejando una distribución menos concentrada en esas regiones.

En términos generales, los resultados sugieren que la concentración de incidentes puede estar asociada a factores como la población, la urbanización y la actividad de las fuerzas policiales en cada estado.
""")

# -------------------------------
# SECCIÓN: CONCLUSIONES
# -------------------------------
elif section == "Conclusiones":
    st.title(" Conclusiones")

    st.write("""
    ## Conclusiones

A partir del análisis exploratorio del dataset sobre incidentes de muertes causadas por disparos policiales, se lograron identificar diversos patrones relevantes en relación con las características de los casos registrados.

En primer lugar, se evidenció una distribución desigual en términos de raza, donde ciertos grupos presentan una mayor cantidad de casos en comparación con otros. Asimismo, se observó que la mayoría de los incidentes involucran a personas adultas jóvenes, concentrándose principalmente en rangos de edad entre los 20 y 45 años.

En cuanto al género, los resultados muestran una marcada predominancia de casos en hombres, lo que indica una afectación desproporcionada hacia este grupo. Esta tendencia se mantiene incluso al analizar variables relacionadas como el nivel de amenaza.

Respecto al comportamiento durante los incidentes, se identificó que la mayoría de los casos ocurren sin que exista un intento de huida por parte del individuo, lo que sugiere que estos eventos no necesariamente están asociados a situaciones de persecución.

Por otro lado, el análisis del tipo de arma revela que una proporción significativa de los casos involucra armas de fuego, aunque también se presentan situaciones con personas desarmadas o con armas no letales, lo cual resulta relevante en la interpretación de la percepción de amenaza.

En términos temporales, se observaron variaciones en la cantidad de casos a lo largo de los años, lo que permite identificar cambios en la frecuencia de los incidentes en el tiempo. De igual forma, el análisis geográfico evidenció que ciertos estados concentran una mayor cantidad de casos, especialmente aquellos con mayor densidad poblacional.

Finalmente, el análisis de correlación mostró que no existen relaciones lineales significativas entre las variables numéricas disponibles, lo que indica que los factores estudiados deben interpretarse de manera individual dentro del contexto del dataset.

En conjunto, estos hallazgos permiten obtener una visión general del comportamiento de los incidentes registrados, destacando patrones relevantes sin establecer relaciones causales, y demostrando la utilidad del análisis exploratorio de datos como herramienta para la comprensión de fenómenos complejos. """)