# En informacion_por_operador.py

# Importaciones necesarias
from sqlalchemy import create_engine
from config import DATABASE_CONNECTION_URI
import streamlit as st
import pandas as pd
from dataframe import df 
from graphs import grafica_barras_tipo
from functions import get_all_descendants_with_hierarchy, analizar_dataframe, mostrar_ficha_informativa

# Creación del motor de conexión a la base de datos



def run():
    filtered_df = df

    # Encontrando padres únicos
    unique_parents = filtered_df[filtered_df['parent'] != ""][['parent', 'ID Operador']].drop_duplicates()
    parent_options = ['Seleccione un elemento...'] + unique_parents['parent'].tolist()
    selected_parent_name = st.selectbox("Por favor, selecciona un elemento de la siguiente lista:", parent_options, key="parent")

    selected_parent_id = None


    if selected_parent_name != "Seleccione un elemento..." and selected_parent_name != 'MOVIMIENTO CIUDADANO ':
        filtered_unique_parents = unique_parents[unique_parents['parent'] == selected_parent_name]
        if not filtered_unique_parents.empty:
            selected_parent_id = filtered_unique_parents['ID Operador'].values[0]
        else:
            st.error(f"No se encontró un ID Operador para el elemento seleccionado: {selected_parent_name}")
            return

    if selected_parent_id:
        try:
            descendants_df = get_all_descendants_with_hierarchy(filtered_df, selected_parent_id)
            filtered_df = descendants_df

            # Aquí continúa tu lógica para filtrar por Tipo y Responsabilidad...
            # Filtro por tipo
            tipo_options = ['Todos'] + filtered_df['Tipo'].unique().tolist()
            tipo = st.selectbox('Tipo', tipo_options)
            if tipo != 'Todos':
                filtered_df = filtered_df[filtered_df['Tipo'] == tipo]

            # Filtro por responsabilidad
            responsabilidad_options = ['Todos'] + filtered_df['Responsabilidad'].unique().tolist()
            responsabilidad = st.selectbox('Responsabilidad', responsabilidad_options)
            if responsabilidad != 'Todos':
                filtered_df = filtered_df[filtered_df['Responsabilidad'] == responsabilidad]


        except Exception as e:
            st.error(f"Error al procesar la selección: {e}")
            return

    else:
        filtered_df = df

        #filtrar por Tipo
        tipo_options = ['Todos'] + filtered_df['Tipo'].unique().tolist()
        tipo = st.selectbox('Tipo', tipo_options)
        if tipo != 'Todos':
            filtered_df = filtered_df[filtered_df['Tipo'] == tipo]
        

        #filtrar por Responsabilidad
        responsabilidad_options = ['Todos'] + filtered_df['Responsabilidad'].unique().tolist()
        responsabilidad = st.selectbox('Responsabilidad', responsabilidad_options)
        if responsabilidad != 'Todos':
            filtered_df = filtered_df[filtered_df['Responsabilidad'] == responsabilidad]

    mostrar_ficha_informativa(df, selected_parent_id)

    # Mostrar gráfica de barras

    grafica_barras_tipo(filtered_df, 'Tipo')
    grafica_barras_tipo(filtered_df, 'Responsabilidad')


    st.write('### Informe por operador')



    st.dataframe(filtered_df[['Persona', 'Operador', 'Tipo', 'Responsabilidad','cellphone', 'Fecha de Alta', 'Municipio', 'Distrito']])

    


    
