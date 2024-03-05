# En resumen.py

# Importaciones necesarias
from sqlalchemy import create_engine
from config import DATABASE_CONNECTION_URI
import streamlit as st
import pandas as pd
from dataframe import df # Asume que estos ya están definidos
from graphs import create_streamgraph, create_stream_graph_mpl, plot_missing_data, grafica_barras_tipo, visualizar_distritos_con_color, grafica_barras_operadores_con_sin_responsabilidad
from functions import get_all_descendants_with_hierarchy, analizar_dataframe

# Creación del motor de conexión a la base de datos



def run():
    st.title('Resumen Ejecutivo')  # Establece el título de la página

    # Conversión de 'Fecha de Alta' a datetime si aún no lo está
    df['Fecha de Alta'] = pd.to_datetime(df['Fecha de Alta'])

    # Establece el rango mínimo y máximo de las fechas
    min_date, max_date = df['Fecha de Alta'].min(), df['Fecha de Alta'].max()

    # Lista de todas las fechas posibles entre el mínimo y el máximo
    dates = df['Fecha de Alta'].dt.date.unique()

    # Widget de selección de rango de fechas como un slider
    start_date, end_date = st.select_slider(
        "Seleccione el rango de fechas:",
        options=sorted(dates),
        value=(min_date.date(), max_date.date())
    )

    # Filtrar el DataFrame basado en el rango de fechas seleccionado
    filtered_df = df[(df['Fecha de Alta'].dt.date >= start_date) & (df['Fecha de Alta'].dt.date <= end_date)]

    # Encontrando padres únicos
    unique_parents = filtered_df[filtered_df['parent'] != ""][['parent', 'ID Operador']].drop_duplicates()
    parent_options = ['Seleccione un actor...'] + unique_parents['parent'].tolist()
    selected_parent_name = st.selectbox("Por favor, selecciona un elemento de la siguiente lista:", parent_options, key="parent")
   
    if selected_parent_name != "Seleccione un actor..." and selected_parent_name != 'MOVIMIENTO CIUDADANO ':
        try:
            selected_parent_id = unique_parents[unique_parents['parent'] == selected_parent_name]['ID Operador'].values[0]
            descendants_df = get_all_descendants_with_hierarchy(filtered_df, selected_parent_id)
            filtered_df = descendants_df
        except Exception as e:
            st.error(f"Error al procesar la selección: {e}")

 

    # Genera y muestra el Streamgraph con los datos filtrados
    create_stream_graph_mpl(filtered_df)
    streamgraph = create_streamgraph(filtered_df, fecha_column='Fecha de Alta', color_column='Tipo')
    st.altair_chart(streamgraph, use_container_width=True)

    # Mostrar distritos
    visualizar_distritos_con_color(filtered_df)


    

    # Analizar el DataFrame y obtener el resumen
    analysis_summary = analizar_dataframe(filtered_df)


    # Mostrar gráfica operadores:
    

    grafica_barras_operadores_con_sin_responsabilidad(filtered_df, 'Operador', 'Responsabilidad')

    # Construye la ruta absoluta a las imágenes
    streamgraph_path = 'streamgraph.png'
    distritos_path =  "distritos.png"
    barras_path = "barras.png"


    from resumen_pdf import insert_images_into_pdf

    # When the button is clicked, generate the PDF
    if st.button('Generar Resumen Ejecutivo'):
        output_filename = 'resumen_ejecutivo.pdf'
        insert_images_into_pdf(selected_parent_name, start_date, end_date, streamgraph_path, distritos_path, barras_path, output_filename)

        # Provide a download button for the generated PDF
        with open(output_filename, "rb") as file:
            st.download_button(
                label="Descargar Resumen Ejecutivo en PDF",
                data=file,
                file_name=output_filename,
                mime='application/pdf'
            )