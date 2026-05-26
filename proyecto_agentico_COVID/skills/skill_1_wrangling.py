"""
Skill 1: Limpieza y Preparación de Datos (Data Wrangling)
Se encarga de transformar los datos crudos en un formato estructurado y limpio,
listo para ser analizado y procesado por algoritmos matemáticos.
"""
import pandas as pd
import os
from sklearn.preprocessing import LabelEncoder

def ejecutar_data_wrangling(df, base_dir):
    """
    Recibe el DataFrame original y aplica limpieza de datos.
    También guarda una copia limpia en la carpeta datos_procesados/.
    """
    print("    Iniciando limpieza de datos...")

    # 1. Copia de seguridad
    df_clean = df.copy()

    # 2. Curación de Nombres de Columnas
    # Se usan bytes reales que produce la codificacion latin-1 del CSV oficial
    columnas_renombradas = {
        'Fecha de notificaci\x97n':        'Fecha de notificacion',
        'C\x97digo DIVIPOLA departamento':  'Codigo departamento',
        'C\x97digo DIVIPOLA municipio':     'Codigo municipio',
        'Ubicaci\x97n del caso':            'Ubicacion del caso',
        'C\x97digo ISO del pa\x92s':        'Codigo ISO pais',
        'Nombre del pa\x92s':               'Nombre pais',
        'Fecha de inicio de s\x92ntomas':   'Fecha de inicio de sintomas',
        'Fecha de diagn\x97stico':          'Fecha de diagnostico',
        'Fecha de recuperaci\x97n':         'Fecha de recuperacion',
        'Tipo de recuperaci\x97n':          'Tipo de recuperacion',
        'Pertenencia \x8etnica':            'Pertenencia etnica',
        'Nombre del grupo \x8etnico':       'Nombre grupo etnico',
    }
    df_clean.rename(columns=columnas_renombradas, inplace=True)

    # 3. Selección de Características (Feature Selection)
    columnas_a_eliminar = [
        'fecha reporte web', 'ID de caso', 'Fecha de notificacion',
        'Codigo departamento', 'Nombre departamento', 'Codigo municipio',
        'Codigo ISO pais', 'Nombre pais', 'Fecha de inicio de sintomas',
        'Fecha de diagnostico', 'Fecha de recuperacion', 'Tipo de recuperacion',
        'Fecha de muerte', 'Pertenencia etnica', 'Nombre grupo etnico',
        'Unidad de medida de edad', 'Recuperado',
    ]
    df_clean.drop(columns=columnas_a_eliminar, inplace=True, errors='ignore')

    # 4. Limpieza de Valores Nulos
    df_clean.dropna(subset=['Estado', 'Ubicacion del caso', 'Tipo de contagio'], inplace=True)

    # 5. Ingeniería de Características (Feature Engineering) - Target
    def clasificar_gravedad(estado):
        estado_str = str(estado).strip().lower()
        if 'leve' in estado_str or 'asint' in estado_str:
            return 0   # Leve / Asintomatico
        else:
            return 1   # Moderado / Grave / Fallecido

    df_clean['Target_Gravedad'] = df_clean['Estado'].apply(clasificar_gravedad)
    df_clean.drop(columns=['Estado', 'Ubicacion del caso'], inplace=True)

    # 6. Codificación de Variables Categóricas (Label Encoding)
    le = LabelEncoder()
    df_clean['Sexo_encoded']           = le.fit_transform(df_clean['Sexo'].astype(str))
    df_clean['Tipo_contagio_encoded']  = le.fit_transform(df_clean['Tipo de contagio'].astype(str))
    
    # Estandarizar Nombre municipio a mayusculas para evitar inconsistencias de registro
    df_clean['Nombre municipio']       = df_clean['Nombre municipio'].astype(str).str.strip().str.upper()
    df_clean['Municipio_encoded']      = le.fit_transform(df_clean['Nombre municipio'])


    df_clean.drop(columns=['Sexo', 'Tipo de contagio', 'Nombre municipio'], inplace=True)

    # 7. Guardar resultados en la carpeta correspondiente
    ruta_procesados = os.path.join(base_dir, 'datos_procesados')
    os.makedirs(ruta_procesados, exist_ok=True)
    df_clean.to_csv(os.path.join(ruta_procesados, 'dataset_limpio_para_modelo.csv'), index=False)

    print(f"    Limpieza completada. Filas: {df_clean.shape[0]} | Columnas: {df_clean.shape[1]}")
    print("    Dataset limpio guardado en 'datos_procesados/dataset_limpio_para_modelo.csv'.")

    return df_clean
