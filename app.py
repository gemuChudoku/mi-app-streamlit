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
@st.cache_data
def load_data():
    return pd.read_csv("https://raw.githubusercontent.com/gemuChudoku/Archivos_csv/refs/heads/main/Social_media_impact_on_life.csv")  # 👈 cambia esto

df = load_data()

# -------------------------------
# SIDEBAR (NAVEGACIÓN)
# -------------------------------
st.sidebar.title("📊 Navegación")

section = st.sidebar.selectbox(
    "Ir a:",
    [
        "Inicio",
        "Uso diario de redes sociales", 
        "Impacto general",
        "Plataformas",
        "Edad vs Uso",
        "Rendimiento académico",
        "Salud Mental",
        "Sueño",
        "Correlación",
        "Conclusiones"
    ]
)

# -------------------------------
# SECCIÓN: INICIO
# -------------------------------
if section == "Inicio":
    st.title("📊 Análisis del uso de IA en estudiantes")

    st.write("""
    ## Introducción al Dataset

En la actualidad, el uso de herramientas basadas en inteligencia artificial ha crecido de manera significativa en el entorno educativo, transformando la forma en que los estudiantes acceden a la información, realizan tareas y desarrollan sus actividades académicas. Este dataset tiene como propósito analizar el impacto de estas tecnologías en diferentes aspectos del rendimiento y bienestar estudiantil.

El análisis se centra en comprender cómo el uso de la inteligencia artificial influye en el desempeño académico, explorando si existe una relación directa entre el tiempo de uso y las calificaciones obtenidas. Asimismo, se busca identificar posibles patrones de dependencia o uso excesivo (adicción) y su relación con factores como la salud mental y la calidad del sueño.

Además, este conjunto de datos permite evaluar si las herramientas de inteligencia artificial representan un apoyo efectivo para el aprendizaje o si, por el contrario, pueden generar efectos negativos en los estudiantes. A través de este análisis, se pretende responder preguntas clave sobre el equilibrio entre el beneficio tecnológico y sus posibles riesgos.

    """)

    st.subheader("Vista del dataset")
    st.dataframe(df.head())

    st.metric("Promedio de uso diario", round(df["Avg_Daily_Usage_Hours"].mean(), 2))


#------------------------------------
# uso diario redes
#----------------------------------


elif section == "Uso diario de redes sociales":
    st.title("📱 Uso diario de redes sociales")

    # Crear bins manuales
    bins = np.arange(0, 10, 1)
    df["Uso_Bin"] = pd.cut(
        df["Avg_Daily_Usage_Hours"],
        bins=bins,
        right=False,
        labels=[f"{i}-{i+1}" for i in range(0, 9)]
    )

    usage_counts = df["Uso_Bin"].value_counts().sort_index().reset_index()
    usage_counts.columns = ["Rango", "Cantidad"]

    # Identificar el máximo
    max_value = usage_counts["Cantidad"].max()

    # Crear color dinámico
    usage_counts["Color"] = usage_counts["Cantidad"].apply(
        lambda x: "#EE6055" if x == max_value else "#60D394"
    )

    fig = px.bar(
        usage_counts,
        x="Rango",
        y="Cantidad",
        color="Rango",
        color_discrete_sequence=usage_counts["Color"],
        title="Distribución del uso diario"
    )

    # Hover personalizado
    fig.update_traces(
        hovertemplate="Rango: %{x}<br>Estudiantes: %{y}"
    )

    # Quitar leyenda (opcional)
    fig.update_layout(showlegend=False)

    st.plotly_chart(fig)

    st.write("""### Interpretación: Distribución del uso diario

La gráfica muestra la distribución de las horas de uso diario entre los estudiantes, agrupadas en intervalos de tiempo. Se observa que el mayor número de estudiantes se concentra en el rango de **4 a 5 horas**, lo que indica que este es el nivel de uso más común dentro del dataset.

Adicionalmente, los intervalos de **5 a 6 horas** y **3 a 4 horas** también presentan una alta frecuencia, seguidos por el rango de **6 a 7 horas**. Esto sugiere que la mayoría de los estudiantes se encuentra en un nivel de uso moderado a relativamente alto, concentrándose principalmente entre las 3 y 7 horas diarias.

A medida que se avanza hacia los extremos (niveles muy bajos o muy altos de uso), la cantidad de estudiantes disminuye, lo que indica que estos comportamientos son menos frecuentes dentro de la población analizada.
""")

#-------------------------------------------
#impacto general
#-------------------------------------------


elif section == "Impacto general":
    st.title("⚖️ Impacto general del uso de IA")

    # Orden lógico
    order = ["Negative", "Neutral", "Positive"]
    impact_counts = df["Overall_Impact"].value_counts().reindex(order).reset_index()
    impact_counts.columns = ["Impacto", "Cantidad"]

    # Colores semánticos
    color_map = {
        "Negative": "#E24B4A",
        "Neutral": "#FED766",
        "Positive": "#1D9E75"
    }

    fig = px.bar(
        impact_counts,
        x="Impacto",
        y="Cantidad",
        color="Impacto",
        color_discrete_map=color_map,
        title="Distribución del impacto del uso de IA"
    )

    # Hover personalizado
    fig.update_traces(
        hovertemplate="Impacto: %{x}<br>Estudiantes: %{y}"
    )

    st.plotly_chart(fig)
    
    st.write("""### Interpretación: Impacto general del uso de IA

La gráfica muestra la distribución del impacto general percibido por los estudiantes frente al uso de herramientas de inteligencia artificial, clasificado en tres categorías: negativo, neutral y positivo.

Se observa una clara diferencia en la cantidad de estudiantes entre las categorías, lo que permite identificar la tendencia predominante en la percepción del impacto. Esta distribución evidencia que el uso de IA no genera un efecto uniforme, sino que depende de la experiencia individual de cada estudiante.

La presencia de una proporción considerable en la categoría negativa sugiere que una parte importante de los estudiantes percibe efectos adversos, lo cual es coherente con los análisis previos donde se identificó una relación entre mayor uso, menor cantidad de horas de sueño y un menor puntaje de salud mental.

Por otro lado, la categoría neutral indica que, para muchos estudiantes, el impacto no es claramente definido, lo que puede estar asociado a un uso moderado o a una percepción equilibrada entre beneficios y desventajas.""")


#-----------------------------------------------------------
# plataformas mas usadas
#-----------------------------------------------------------



elif section == "Plataformas":
    st.title("📱 Plataformas más utilizadas")

    platform_counts = df["Most_Used_Platform"].value_counts().reset_index()
    platform_counts.columns = ["Plataforma", "Cantidad"]

    fig = px.bar(
        platform_counts,
        x="Plataforma",
        y="Cantidad",
        title="Plataformas más utilizadas",
    )

    top_platform = df["Most_Used_Platform"].value_counts().idxmax()
    top_count = df["Most_Used_Platform"].value_counts().max()

    st.metric("Plataforma más usada", top_platform, f"{top_count} estudiantes")

    st.plotly_chart(fig)

    st.write("""### Interpretación: Plataformas más utilizadas

 Se observa una clara concentración en ciertas plataformas, destacándose **Instagram** como la más utilizada, seguida por **TikTok** y **Facebook**.

Esta tendencia sugiere una preferencia por plataformas altamente visuales e interactivas, especialmente aquellas que ofrecen contenido corto y dinámico. La diferencia entre estas plataformas principales y el resto es significativa, lo que indica que el uso no está distribuido de manera uniforme, sino que se concentra en un grupo reducido de aplicaciones dominantes.

Por otro lado, plataformas como **LinkedIn**, **Twitter** y **YouTube** presentan un uso intermedio, lo que podría estar relacionado con fines más específicos como el networking, la información o el consumo de contenido educativo.

Finalmente, se observa que algunas plataformas como **WhatsApp**, **WeChat**, **LINE**, **VKontakte** y **KakaoTalk** tienen una presencia mínima en el dataset, lo cual podría deberse a factores geográficos, culturales o al enfoque académico del estudio.
""")


#----------------------------------------------
#edad vs uso
#--------------------------------------------

elif section == "Edad vs Uso":
    st.title("👤 Uso promedio según la edad")

    # Agrupar datos
    avg_age_usage = df.groupby("Age")["Avg_Daily_Usage_Hours"].mean().reset_index()

    # Crear gráfica
    fig = px.line(
        avg_age_usage,
        x="Age",
        y="Avg_Daily_Usage_Hours",
        markers=True,
        title="Uso promedio de IA/Redes Sociales según la edad"
    )

    # Hover personalizado
    fig.update_traces(
        hovertemplate="Edad: %{x}<br>Horas promedio: %{y:.2f}"
    )

    # Ajustar eje Y
    fig.update_layout(
        yaxis=dict(range=[0, avg_age_usage["Avg_Daily_Usage_Hours"].max() * 1.1]),
        xaxis_title="Edad",
        yaxis_title="Horas promedio de uso"
    )

    st.plotly_chart(fig)

    st.write("""###  Interpretación: Uso de IA/Redes Sociales según la edad

La gráfica muestra la relación entre la edad de los estudiantes y el promedio de horas de uso diario de herramientas de inteligencia artificial.

Se observa que el uso se mantiene relativamente **estable a lo largo de todas las edades analizadas**, con valores cercanos a las 5 horas diarias en promedio. No se presentan variaciones significativas, aunque se aprecia una ligera disminución del uso a medida que aumenta la edad, especialmente alrededor de los 22 a 23 años.

Sin embargo, esta variación es mínima, lo que sugiere que la edad no es un factor determinante en la cantidad de uso de herramientas de inteligencia artificial dentro del rango analizado.

Este comportamiento indica que el uso de IA está bastante generalizado entre los estudiantes, independientemente de su edad, lo que refuerza la idea de que estas tecnologías forman parte del entorno académico cotidiano.
""")


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
# ia y salud mental
#------------------------------------------------


elif section == "Salud Mental":
    st.title("🧠 Uso de IA vs Salud Mental")

    color_map = {
        "Negative": "#E24B4A",
        "Neutral": "#FED766",
        "Positive": "#1D9E75"
    }

    fig = go.Figure()

    # Scatter por categoría
    for impact, color in color_map.items():
        subset = df[df["Overall_Impact"] == impact]
        fig.add_trace(go.Scatter(
            x=subset["Avg_Daily_Usage_Hours"],
            y=subset["Mental_Health_Score"],
            mode='markers',
            name=impact,
            marker=dict(color=color, opacity=0.6)
        ))

    # Línea de tendencia global
    z = np.polyfit(df["Avg_Daily_Usage_Hours"], df["Mental_Health_Score"], 1)
    p = np.poly1d(z)

    x_range = np.linspace(df["Avg_Daily_Usage_Hours"].min(), df["Avg_Daily_Usage_Hours"].max(), 100)

    fig.add_trace(go.Scatter(
        x=x_range,
        y=p(x_range),
        mode='lines',
        name='Tendencia',
        line=dict(color='black', dash='dash')
    ))

    fig.update_layout(
        title="Relación entre uso de IA y salud mental",
        xaxis_title="Horas promedio de uso diario",
        yaxis_title="Puntaje de salud mental"
    )

    st.plotly_chart(fig)
    st.write("""### 🧠 Interpretación: Uso de IA vs Salud Mental

La visualización muestra una relación inversa entre el tiempo de uso diario de herramientas de inteligencia artificial y el puntaje de salud mental de los estudiantes.

La línea de tendencia descendente indica que, a medida que aumentan las horas de uso, el puntaje de salud mental tiende a disminuir. Esto sugiere una posible asociación negativa entre el uso intensivo de estas tecnologías y el bienestar psicológico de los estudiantes.

Sin embargo, también se observa que los datos presentan cierta dispersión, lo que indica que la relación no es completamente determinante y que existen casos en los que estudiantes con alto uso mantienen niveles de salud mental relativamente estables.

Este comportamiento sugiere que, aunque el uso excesivo de herramientas de inteligencia artificial podría estar relacionado con efectos negativos en la salud mental.""")


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


elif section == "Correlación":
    st.title("📊 Matriz de correlación")

    # Seleccionar variables numéricas
    numeric_df = df[
        [
            "Avg_Daily_Usage_Hours",
            "Sleep_Hours_Per_Night",
            "Mental_Health_Score"
        ]
    ]

    corr_matrix = numeric_df.corr()

    # Crear heatmap
    fig = px.imshow(
        corr_matrix,
        text_auto=True,  # 👈 muestra los valores
        color_continuous_scale="RdBu_r",
        title="Matriz de correlación entre variables"
    )

    # Ajustes
    fig.update_layout(
        xaxis_title="Variables",
        yaxis_title="Variables"
    )

    st.plotly_chart(fig)
    st.write("""###  Interpretación: Matriz de Correlación

La matriz de correlación permite identificar la relación entre las principales variables numéricas del dataset: el uso diario de inteligencia artificial, las horas de sueño y el puntaje de salud mental.

En primer lugar, se observa una **fuerte correlación negativa (-0.82)** entre el uso diario de IA y las horas de sueño. Esto indica que, a medida que aumenta el tiempo de uso, las horas de descanso tienden a disminuir de manera significativa.

De igual forma, existe una **correlación negativa aún más fuerte (-0.83)** entre el uso de IA y el puntaje de salud mental. Este resultado sugiere que un mayor uso está asociado con un menor bienestar psicológico en los estudiantes.

Por otro lado, se identifica una **correlación positiva alta (0.79)** entre las horas de sueño y la salud mental, lo que indica que dormir más está relacionado con mejores niveles de bienestar emocional.
""")
# -------------------------------
# SECCIÓN: CONCLUSIONES
# -------------------------------
elif section == "Conclusiones":
    st.title("🏁 Conclusiones")

    st.write("""
    ## 🏁 Conclusiones Generales

A partir del análisis exploratorio del dataset, se identificaron patrones relevantes sobre el impacto del uso de herramientas de inteligencia artificial en el entorno estudiantil.

En primer lugar, se evidenció que el **tiempo de uso diario** es un factor clave, ya que niveles más altos de uso se asocian con una **disminución en las horas de sueño** y un **menor puntaje de salud mental**. Estas relaciones fueron confirmadas tanto en las visualizaciones individuales como en la matriz de correlación, donde se observaron asociaciones negativas fuertes.

Asimismo, se identificó una **relación positiva entre las horas de sueño y la salud mental**, lo que sugiere que el descanso adecuado juega un papel importante en el bienestar de los estudiantes. Esto permitió establecer una posible cadena de impacto: un mayor uso de IA podría reducir las horas de sueño, lo cual a su vez influye negativamente en la salud mental.

En cuanto al rendimiento académico, los resultados indican que los estudiantes que reportan una afectación tienden a presentar un **mayor uso diario**, lo que sugiere que el uso intensivo podría estar relacionado con una percepción de impacto en su desempeño.

Por otro lado, el análisis por edad mostró que el uso de IA es **relativamente uniforme entre los estudiantes**, lo que indica que esta variable no representa una diferencia significativa en los hábitos de uso. Esto refuerza la idea de que la inteligencia artificial está ampliamente integrada en el entorno académico, independientemente de la edad.

Finalmente, la percepción del impacto general evidencia que el uso de IA no tiene un efecto uniforme, sino que varía entre los estudiantes, dependiendo de factores como la intensidad de uso y los hábitos individuales.

En conjunto, estos hallazgos resaltan la importancia de promover un **uso equilibrado y consciente de las herramientas de inteligencia artificial y redes sociales**, maximizando sus beneficios académicos mientras se minimizan sus posibles efectos negativos en el bienestar y los hábitos de los estudiantes.
    """)