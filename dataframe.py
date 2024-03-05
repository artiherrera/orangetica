# dataframe.py

from sqlalchemy import create_engine
import pandas as pd
from babel.dates import format_date
from config import DATABASE_CONNECTION_URI
from querys import query_personas
import os

engine = create_engine(DATABASE_CONNECTION_URI)

df = pd.read_sql(query_personas, engine)

df['ID'] = df['p_id'].astype(int)
df['ID Operador'] = df['ID Operador'].fillna(-1).astype(int)
df['parent'] = df['Operador'].astype(str)
df['Persona'] = df['Persona'].astype(str)
df['Responsabilidad'] = df['Responsabilidad'].astype(str)
df['Fecha de Alta'] = pd.to_datetime(df['Fecha de Alta'])

ruta_archivo = os.path.join('datasets', 'territorio.csv')
df_territorio = pd.read_csv(ruta_archivo)


df_territorio['ID'] = df_territorio['ID'].astype(int)

# Realizar el merge para asociar información territorial a cada persona en df
df_merged = pd.merge(df, df_territorio[['ID', 'Estado', 'Distrito', 'Municipio']], how='left', left_on='ID', right_on='ID')

# Optimizar la propagación de la información territorial de padres a hijos
# Crear un diccionario para mapear cada ID a su información territorial
info_territorial = df_territorio.set_index('ID')[['Estado', 'Distrito', 'Municipio']].to_dict('index')

# Función para actualizar la información de los hijos basada en el mapeo
def actualizar_info_hijos(df):
    for index, row in df.iterrows():
        # Si el registro ya tiene información territorial, omitir
        if pd.notna(row['Estado']):
            continue
        # Obtener información del padre si está disponible
        id_padre = row['ID Operador']
        if id_padre in info_territorial:
            info_padre = info_territorial[id_padre]
            for campo in ['Estado', 'Distrito', 'Municipio']:
                # Actualizar solo si la información no está presente
                if pd.isna(row[campo]):
                    df.at[index, campo] = info_padre.get(campo)
    return df

# Aplicar la función para actualizar la información territorial
df_actualizado = actualizar_info_hijos(df_merged)

# Sustituir df con la versión actualizada
df = df_actualizado