"""
Skill 3: Modelado Predictivo (Machine Learning)
Se encarga de entrenar modelos matemáticos capaces de predecir la gravedad
de un caso (Target_Gravedad) basándose en las variables limpias.
"""
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, f1_score
import warnings
warnings.filterwarnings('ignore') # Limpieza de consola

def ejecutar_modelo_predictivo(df_clean):
    """
    Recibe el DataFrame limpio, divide los datos estratégicamente, 
    entrena modelos competidores, los evalúa usando F1-Score, 
    selecciona al ganador y muestra el reporte de métricas.
    """
    print("    Preparando algoritmos de Machine Learning...")
    
    # 1. Separación X (Características) e y (Objetivo)
    X = df_clean.drop(columns=['Target_Gravedad'])
    y = df_clean['Target_Gravedad']
    
    # 2. División Estratificada (Train/Test Split)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # 3. Inicialización de Algoritmos (con Balanceo de Clases)
    modelo_rl = LogisticRegression(class_weight='balanced', random_state=42)
    modelo_rf = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
    
    # 4. Entrenamiento
    print("    -> Entrenando Regresión Logística...")
    modelo_rl.fit(X_train, y_train)
    
    print("    -> Entrenando Random Forest...")
    modelo_rf.fit(X_train, y_train)
    
    # 5. Predicción en Test
    pred_rl = modelo_rl.predict(X_test)
    pred_rf = modelo_rf.predict(X_test)
    
    # 6. Evaluación mediante F1-Score
    f1_rl = f1_score(y_test, pred_rl, average='weighted')
    f1_rf = f1_score(y_test, pred_rf, average='weighted')
    
    # 7. Decisión y Reporte
    print("\n      [Evaluación] Puntajes F1 (F1-Score):")
    print(f"      - Regresión Logística : {f1_rl:.4f}")
    print(f"      - Random Forest       : {f1_rf:.4f}")
    
    if f1_rf >= f1_rl:
        mejor_modelo, nombre_ganador, pred_final = modelo_rf, "Random Forest", pred_rf
    else:
        mejor_modelo, nombre_ganador, pred_final = modelo_rl, "Regresión Logística", pred_rl
        
    print(f"\n    Modelo Ganador Seleccionado: {nombre_ganador}")
    print("\n      [Reporte Final del Modelo]")
    reporte = classification_report(y_test, pred_final, target_names=['Leve (0)', 'Grave (1)'])
    print(reporte)
    
    print("    Modelado completado.")
    
    metricas_dict = {
        'nombre_ganador': nombre_ganador,
        'f1_rl': f1_rl,
        'f1_rf': f1_rf,
        'reporte_clasificacion': reporte
    }
    return mejor_modelo, metricas_dict

