import pandas as pd
import streamlit as st
from sqlalchemy import create_engine


def get_all_descendants_with_hierarchy(df2, parent_id):
    # Inicializar la lista de IDs para procesar con el parent_id inicial
    ids_to_process = [parent_id]
    # Inicializar un conjunto para rastrear todos los IDs de descendientes encontrados para evitar duplicados
    descendants_ids = set()

    while ids_to_process:
        # Obtener el próximo lote de hijos directos basado en los IDs actuales a procesar
        current_batch = df2[df2['ID Operador'].isin(ids_to_process)]
        # Extraer los IDs de estos hijos y agregarlos al conjunto de descendientes si no están ya presentes
        new_ids = set(current_batch['ID'].unique())
        # Actualizar la lista de IDs a procesar con los nuevos IDs encontrados que no han sido procesados aún
        ids_to_process = list(new_ids - descendants_ids)
        # Actualizar el conjunto de todos los IDs de descendientes encontrados
        descendants_ids.update(new_ids)

    # Filtrar el DataFrame original para incluir solo las filas de los descendientes identificados
    descendants_df = df2[df2['ID'].isin(descendants_ids)]
    return descendants_df



import streamlit as st
import pandas as pd

def analizar_dataframe(df):
    # Análisis del DataFrame
    total_filas = len(df)
    filas_completas = df.dropna().shape[0]
    filas_incompletas = total_filas - filas_completas
    columna_operador = 'ID Operador' if 'ID Operador' in df.columns else 'OperadorID'
    operadores_unicos = df[columna_operador].nunique()
    hijos = df[df[columna_operador].isin(df['ID'])][columna_operador].nunique()

    # Mostrar los resultados en Streamlit
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de filas", total_filas)
        st.metric("Filas completas", filas_completas)
    with col2:
        st.metric("Filas incompletas", filas_incompletas)
        st.metric("Actores únicos", operadores_unicos)
    with col3:
        st.metric("Actores con simpatizantes", hijos)

    analysis_summary = {}
        
    # Intenta realizar el análisis
    try:
        # Aquí tu lógica de análisis existente...
        # Por ejemplo:
        total_filas = len(df)
        filas_completas = df.dropna().shape[0]
        filas_incompletas = total_filas - filas_completas
        # Suponiendo que estos son los cálculos que deseas incluir en tu resumen
        
        # Actualiza el diccionario con los resultados
        analysis_summary = {
            "Total de actores": total_filas,
            "Filas completas": filas_completas,
            "Filas incompletas": filas_incompletas,
            # Añade aquí otros resultados del análisis
        }
    except Exception as e:
        # Maneja posibles errores durante el análisis
        print(f"Error al analizar el DataFrame: {e}")
    
    # Retorna el resumen del análisis
    return analysis_summary



def mostrar_ficha_informativa(df, selected_id):
    # Filtra el DataFrame para el ID seleccionado
    df_filtrado = df[df['ID'] == selected_id]
    
    # Verifica si el DataFrame filtrado no está vacío
    if not df_filtrado.empty:
        # Selecciona la primera fila como representante (en caso de múltiples filas)
        ficha = df_filtrado.iloc[0]

        # Cambia el nombre de las columnas para la presentación
        ficha_presentacion = {
            "ID": ficha["ID"],
            "Nombre": ficha["Persona"],
            "Actor": ficha["Operador"],
            "Celular": ficha["cellphone"],  # Asume que ya tienes esta columna en tu DataFrame
            "Sección": ficha["Sección"],  # Asume que ya tienes esta columna en tu DataFrame
            "Responsabilidad": ficha["Responsabilidad"],
            "Tipo": ficha["Tipo"],
            "Fecha de Alta": ficha["Fecha de Alta"].strftime('%Y-%m-%d')  # Formato de fecha
        }
        
        # Muestra la ficha informativa
        st.write("### Ficha Informativa")
        for key, value in ficha_presentacion.items():
            st.text(f"{key}: {value}")
    else:
        st.write("No se encontró información para el elemento seleccionado.")



def heredar_info_de_padres(df, df_with_hierarchy, selected_parent_id):
   
    datos_padre = df[df['ID'] == selected_parent_id][['Municipio', 'Estado', 'Distrito']].iloc[0]

    for index, row in df_with_hierarchy.iterrows():
       
        if row['Jerarquía'] > 0:  # Si no es el nivel más alto (el padre), entonces es un hijo y debe heredar la información
            df_with_hierarchy.at[index, 'Municipio'] = datos_padre['Municipio']
            df_with_hierarchy.at[index, 'Estado'] = datos_padre['Estado']
            df_with_hierarchy.at[index, 'Distrito'] = datos_padre['Distrito']

    return df_with_hierarchy

