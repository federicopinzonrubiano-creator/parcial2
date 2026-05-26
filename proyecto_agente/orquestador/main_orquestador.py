"""
Agente Analítico Orquestador - Proyecto COVID-19 Caldas
Este script actúa como el controlador principal que dirige el flujo de datos 
a través de las diferentes habilidades (Skills) del agente.
"""
import pandas as pd
import sys
import os

# Aseguramos que Python pueda encontrar la carpeta 'skills' agregando la ruta base
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Importación de las Skills (Módulos especializados)
from skills.skill_1_wrangling import ejecutar_data_wrangling
from skills.skill_2_eda import ejecutar_analisis_exploratorio
from skills.skill_3_modelado import ejecutar_modelo_predictivo
from skills.skill_4_reporte import generar_reporte_ejecutivo

class AgenteOrquestador:
    """
    Clase que representa al Agente Principal. 
    Se encarga de cargar el dataset y pasarlo secuencialmente por las fases de:
    1. Limpieza de datos (Wrangling)
    2. Análisis Exploratorio (EDA)
    3. Modelado Predictivo (Machine Learning)
    """
    def __init__(self, ruta_dataset):
        self.ruta_dataset = ruta_dataset
        self.datos_crudos = None
        self.datos_limpios = None
        self.modelo_final = None
        self.metricas = None

    def ejecutar_pipeline(self):
        print("="*60)
        print("[Agente Orquestador] Iniciando el pipeline analitico...")
        print("="*60)
        
        # 1. Cargar Datos Crudos
        print("\n[Paso 0] Cargando dataset original desde 'datos_crudos/'...")
        ruta_completa = os.path.join(BASE_DIR, self.ruta_dataset)
        try:
            self.datos_crudos = pd.read_csv(ruta_completa, sep=';', encoding='latin-1', on_bad_lines='skip')
        except FileNotFoundError:
            print(f"Error: No se encontro el dataset en la ruta {ruta_completa}")
            return
            
        # 2. Skill 1: Preparación de datos
        print("\n[Paso 1] Activando Skill 1: Data Wrangling...")
        self.datos_limpios = ejecutar_data_wrangling(self.datos_crudos, BASE_DIR)
        
        # 3. Skill 2: EDA
        print("\n[Paso 2] Activando Skill 2: Analisis Exploratorio...")
        ejecutar_analisis_exploratorio(self.datos_limpios, BASE_DIR, df_crudo=self.datos_crudos)
        
        # 4. Skill 3: Modelado
        print("\n[Paso 3] Activando Skill 3: Modelado Predictivo...")
        self.modelo_final, self.metricas = ejecutar_modelo_predictivo(self.datos_limpios)
        
        # 5. Skill 4: Reporte Ejecutivo
        generar_reporte_ejecutivo(self.metricas, BASE_DIR)
        
        print("\n" + "="*60)
        print("[Agente Orquestador] Pipeline finalizado con exito.")
        print("="*60)


# Punto de entrada de la ejecución
if __name__ == "__main__":
    # La ruta ahora es relativa a la carpeta de datos crudos
    orquestador = AgenteOrquestador(os.path.join('datos_crudos', 'Casos_positivos_de_COVID-19_en_Caldas.csv'))
    orquestador.ejecutar_pipeline()
