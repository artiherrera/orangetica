import altair as alt
import matplotlib.pyplot as plt

def create_streamgraph(df, fecha_column='Fecha de Alta', color_column='Tipo'):
    # Define una escala de color personalizada para cada tipo
    tipo_colores = {
        "Estructura": "#fb8500",  # Azul
        "Presimpatizante": "#8ecae6",  # Naranja
        "Simpatizante": "#ffb703",  # Verde
    }

    chart = alt.Chart(df).mark_area(
        interpolate='monotone',
        tension=1
    ).encode(
        x=alt.X(fecha_column + ':T', axis=alt.Axis(title='Fecha de Alta')),
        y=alt.Y('count()', stack='center', axis=None),
        # Personaliza la escala de colores usando 'domain' y 'range'
        color=alt.Color(color_column + ':N',
                        scale=alt.Scale(domain=list(tipo_colores.keys()),
                                        range=list(tipo_colores.values())),
                        legend=alt.Legend(title="Tipos")),
        tooltip=[fecha_column, color_column]
    ).properties(
        width=600,
        height=400
    )
    
    return chart

import altair as alt


# Crear streamgraph con Matplotlib


import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import locale
import platform
from matplotlib import rcParams

# Configurar el entorno para español (ajustar según tu sistema operativo)
try:
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8' if platform.system() == 'Linux' else 'es_ES')
except:
    pass

# Configurar Matplotlib para usar la fuente Roboto y el color gris para todo el texto
rcParams['font.family'] = 'Helvetica Neue, Helvetica, Arial, sans-serif'
rcParams['text.color'] = '#757575'  # Ejemplo de color gris, ajustar al tono específico de gris deseado
rcParams['font.size'] = 10  # Ajustar al tamaño de fuente deseado


def create_stream_graph_mpl(df, fecha_column='Fecha de Alta', color_column='Tipo'):
    # Definición de colores por tipo
    tipo_colores = {
        "Estructura": "#fb8500",
        "Presimpatizante": "#8ecae6",
        "Simpatizante": "#ffb703",
    }

    plt.figure(figsize=(10, 4))  # Mantener el tamaño original de la figura

    # Preparación de datos
    df[fecha_column] = pd.to_datetime(df[fecha_column])
    df.sort_values(by=fecha_column, inplace=True)

    # Formatear las fechas en el DataFrame para usar el formato deseado
    df['FechaFormateada'] = df[fecha_column].dt.strftime('%d/%b/%Y')

    # Ordenar y asegurar unicidad en las fechas formateadas para el eje X
    fechas_unicas = df['FechaFormateada'].unique()
    
    # Inicializar una lista para almacenar los datos de cada 'Tipo'
    ys = []
    for tipo in tipo_colores.keys():
        counts = df[df[color_column] == tipo].groupby('FechaFormateada').size()
        counts_reindexed = counts.reindex(fechas_unicas, fill_value=0).to_numpy()
        ys.append(counts_reindexed)

    # Crear el stackplot con todos los datos
    plt.stackplot(range(len(fechas_unicas)), ys, labels=tipo_colores.keys(), colors=tipo_colores.values(), baseline='wiggle', alpha=0.5)
    
    # Determinar cada cuántas fechas se mostrará una etiqueta
    step = max(len(fechas_unicas) // 16, 1)
    xticks = np.arange(0, len(fechas_unicas), step)
    xticklabels = [fechas_unicas[i] if i in xticks else '' for i in xticks]

    # Ajustar las etiquetas del eje X
    plt.xticks(xticks, xticklabels, rotation='vertical', color='grey', fontsize=8)  # Establecer color de las etiquetas del eje X

    # Quitar las etiquetas y los ticks del eje Y
    ax = plt.gca()
    ax.set_yticklabels([])
    ax.set_yticks([])
    
    plt.ylabel('', color='grey', fontsize=8)  # Establecer color de la etiqueta del eje Y
    plt.title('Flujo de registros por tipo', color='grey', fontsize=12)  # Establecer color del título
    legend = plt.legend(loc='upper left', frameon=False)
    plt.setp(legend.get_texts(), color='grey', fontsize=8)  # Establecer color de las leyendas

    # Cambiar el color de las marcas del eje X y Y a gris
    ax = plt.gca()
    ax.tick_params(axis='x', colors='grey')
    ax.tick_params(axis='y', colors='grey')

    # Eliminar bordes
    for spine in ax.spines.values():
        spine.set_visible(False)

    plt.tight_layout()
    
    # Guardar grafica
    plt.savefig('streamgraph.png', format='png', bbox_inches='tight', pad_inches=0.1)

# Graficar datos faltantes
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def plot_missing_data(df):
    # Calcular el número de datos faltantes por columna
    missing_data = df.isnull().sum()
    missing_data = missing_data[missing_data > 0]  # Filtrar columnas con datos faltantes
    missing_data.sort_values(inplace=True)
    
    # Crear la figura y el eje con Matplotlib
    fig, ax = plt.subplots(figsize=(10, 8))  # Ajustar al tamaño deseado
    
    # Crear la gráfica de barras horizontal
    missing_data.plot(kind='barh', color='skyblue', ax=ax)
    
    # Configurar título y etiquetas con estilos personalizados
    ax.set_title('Número de Datos Faltantes por Columna', color='grey', fontsize=12)
    ax.set_xlabel('Número de Datos Faltantes', color='grey', fontsize=10)
    ax.set_ylabel('Columnas', color='grey', fontsize=10)
    
    # Configurar los ticks del eje X y Y con colores y tamaños de fuente personalizados
    ax.tick_params(axis='x', colors='grey', labelsize=8)
    ax.tick_params(axis='y', colors='grey', labelsize=8)
    
    # Añadir una cuadrícula para mejorar la legibilidad
    ax.grid(axis='x', color='grey', linestyle='--', linewidth=0.5)
    
    # Ajustar el layout para asegurarse de que todo encaje bien
    fig.tight_layout()
    
    # Mostrar la gráfica en Streamlit
    st.pyplot(fig)





def grafica_barras_tipo(df, columna):
    # Preparar los datos
    datos = df[columna].value_counts()

    # Ordenar datos
    datos = datos.sort_values(ascending=True)

    #Seleccionar primeros 100 datos
    datos = datos.tail(100)
    
    # Calcular el alto de la figura basado en el número de barras
    # Asumiendo que cada barra necesita un mínimo de 0.5 pulgadas de espacio vertical para evitar superposiciones
    altura_por_barra = 0.3  # Ajusta este valor según sea necesario para mejorar la visualización
    fig_alto = max(len(datos) * altura_por_barra, 2)  # Asegura un mínimo de 2 pulgadas para figuras con pocas barras
    
    # Crear la gráfica de barras horizontal con tamaño ajustado
    fig, ax = plt.subplots(figsize=(10, fig_alto))  # El ancho se mantiene, el alto se ajusta
    
    barras = ax.barh(datos.index, datos.values, color='orange')
    
    # Añadir títulos y etiquetas
    ax.set_xlabel(' ')
    ax.set_ylabel(' ')
    ax.set_title(f'Registros por {columna}')

    # Quitar bordes de la gráfica
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    #Quitar xticks lables y xticks
    ax.set_xticks([])
    ax.set_xticklabels([])
    
    # Añadir el valor de cada barra al lado derecho de ella para mejor claridad
    for barra in barras:
        ax.text(barra.get_width(), barra.get_y() + barra.get_height() / 2,
                f' {int(barra.get_width())}',
                va='center', ha='left')
    
    # Guardar gráfica
        
    plt.savefig('barras.png', format='png', bbox_inches='tight', pad_inches=0.1)
    
    st.pyplot(fig)

from adjustText import adjust_text
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import streamlit as st
from geografia import preparar_distritos_con_conteo

def visualizar_distritos_con_color(df, color_inicio='white', color_fin='orange'):
    geo_df = preparar_distritos_con_conteo(df)
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    cmap = LinearSegmentedColormap.from_list("mi_cmap", [color_inicio, color_fin])

    # Añadir borde de distritos. Puedes cambiar 'black' por cualquier color que prefieras
    geo_df.plot(column='Conteo', ax=ax, legend=True,
                legend_kwds={'label': "Cantidad de Actores por Distrito"},
                cmap=cmap, edgecolor='gray', linewidth=0.2)  # Ajusta el ancho de línea si es necesario

    texts = []
    for x, y, label in zip(geo_df.geometry.centroid.x, geo_df.geometry.centroid.y, geo_df['Distrito']):
        texts.append(ax.text(x, y, label, fontsize=8))

    adjust_text(texts, arrowprops=dict(arrowstyle='->', color='white'))

    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    plt.title('Visualización de Distritos por Cantidad de Actores')
    st.pyplot(fig)



import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st  # Asegúrate de haber importado Streamlit

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st  # Asegúrate de haber importado Streamlit

def grafica_barras_operadores_con_sin_responsabilidad(df, columna_operador, columna_responsabilidad):
    # Crear una nueva columna para clasificar cada registro como 'Con Responsabilidad' o 'Sin Responsabilidad'
    df['Clasificación Responsabilidad'] = df[columna_responsabilidad].apply(lambda x: 'Con Responsabilidad' if x != 'Sin Responsabilidad' else 'Sin Responsabilidad')
    
    # Agrupar por 'Operador' y 'Clasificación Responsabilidad', y contar registros
    datos_agrupados = df.groupby([columna_operador, 'Clasificación Responsabilidad']).size().unstack(fill_value=0)

    # Asegurar que ambos, 'Con Responsabilidad' y 'Sin Responsabilidad', estén presentes
    if 'Con Responsabilidad' not in datos_agrupados.columns:
        datos_agrupados['Con Responsabilidad'] = 0
    if 'Sin Responsabilidad' not in datos_agrupados.columns:
        datos_agrupados['Sin Responsabilidad'] = 0

    # Calcular el total de registros por operador y ordenar por este total
    datos_agrupados['Total'] = datos_agrupados.sum(axis=1)
    datos_agrupados = datos_agrupados.sort_values(by='Total', ascending=True).drop(columns=['Total'])
    datos_agrupados = datos_agrupados.tail(51)  # Limitar a los primeros 50 registros para mejorar la visualización

    #Saltarse el primer registro, ya que es el total
    datos_agrupados = datos_agrupados.iloc[1:51]

    
    # Calcular el alto de la figura basado en el número de barras
    altura_por_barra = 0.5  # Ajuste basado en el estilo anterior
    fig_alto = max(len(datos_agrupados) * altura_por_barra, 2)  # Asegura un mínimo de 2 pulgadas para figuras con pocas barras
    
    # Crear la figura para la gráfica
    fig, ax = plt.subplots(figsize=(12, fig_alto))
    datos_agrupados[['Con Responsabilidad', 'Sin Responsabilidad']].plot(kind='barh', stacked=True, color=['orange', 'lightgrey'], ax=ax)
    
    ax.set_xlabel('Cantidad')
    ax.set_ylabel(columna_operador)
    ax.set_title('Conteo de Operadores por Responsabilidad')

    #Ajustar leyendas:
    ax.legend(title='', bbox_to_anchor=(1.05, 1), loc='upper left')

    
    # Quitar bordes de la gráfica y xticks
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.set_xticks([])
    ax.set_xticklabels([])

    # Añadir el valor de cada segmento de las barras apiladas con las etiquetas fuera de las barras
    for bars in ax.containers:
        for bar in bars:
            width = bar.get_width()
            label_x_pos = bar.get_x() + width + 0.5  # Añade un pequeño espacio después del final de la barra para la etiqueta
            ax.text(label_x_pos, bar.get_y() + bar.get_height()/2, f'{int(width)}', va='center', ha='left')

    plt.tight_layout(rect=[0, 0, 0.85, 1])
    
    # Guardar gráfica y mostrar en Streamlit
    plt.savefig('operadores_responsabilidad.png', format='png', bbox_inches='tight', pad_inches=0.1)
    st.pyplot(fig)
