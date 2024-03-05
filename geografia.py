import geopandas as gpd
import pandas as pd
import os

def preparar_distritos_con_conteo(df_conteo):
    ruta_shp = "datasets/DISTRITO_FEDERAL.shp"  # Ruta fija al archivo .shp
    distrito_federal = gpd.read_file(ruta_shp)
    distrito_federal['Distrito'] = range(1, len(distrito_federal) + 1)
    
    conteo_df = df_conteo.groupby('Distrito').size().reset_index(name='Conteo')
    
    distrito_federal_con_conteo = distrito_federal.merge(conteo_df, on='Distrito', how='left').fillna(0)
    return distrito_federal_con_conteo
