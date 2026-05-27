"""
Skill 2: Análisis Exploratorio de Datos (EDA)
Se encarga de generar resúmenes estadísticos en consola y guardar evidencias 
visuales (gráficos) en el sistema de archivos para entender el comportamiento 
de los datos de forma no bloqueante.
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


def generar_tabla_municipios(df_crudo, base_dir):
    """
    Genera una tabla comparativa por municipio mostrando cantidad y porcentaje
    de casos segun estado: Leve, Asintomatico, Moderado, Grave, Fallecido.
    Guarda CSV y dos graficos: barras apiladas + heatmap de correlacion.
    """
    print("\n      [Tabla Comparativa] Casos por Municipio y Estado:")

    df = df_crudo.copy()
    df['Estado'] = df['Estado'].astype(str).str.strip()
    df['Nombre municipio'] = df['Nombre municipio'].astype(str).str.strip().str.upper()


    # --- Tabla pivot: filas = municipio, columnas = estado ---
    tabla = df.pivot_table(
        index='Nombre municipio',
        columns='Estado',
        aggfunc='size',
        fill_value=0
    )

    # Orden de menor a mayor gravedad
    orden_real = ['Leve', 'Asintomático', 'Moderado', 'Grave', 'Fallecido']
    tabla = tabla.reindex(columns=[c for c in orden_real if c in tabla.columns], fill_value=0)

    # Total y porcentaje por municipio
    tabla['Total'] = tabla.sum(axis=1)
    cols_estado = [c for c in orden_real if c in tabla.columns]
    for col in cols_estado:
        tabla[f'% {col}'] = (tabla[col] / tabla['Total'] * 100).round(1)

    print(tabla.to_string())

    # Guardar CSV
    ruta_procesados = os.path.join(base_dir, 'datos_procesados')
    os.makedirs(ruta_procesados, exist_ok=True)
    tabla.to_csv(os.path.join(ruta_procesados, 'tabla_municipios_por_estado.csv'))
    print("\n      Tabla guardada en 'datos_procesados/tabla_municipios_por_estado.csv'.")

    carpeta_evidencias = os.path.join(base_dir, 'graficos')
    os.makedirs(carpeta_evidencias, exist_ok=True)

    # --- Grafico A: Barras apiladas por municipio ---
    colores = ['#2ecc71', '#a8e6cf', '#f39c12', '#e74c3c', '#7f0000']
    ax = tabla[cols_estado].plot(
        kind='bar',
        stacked=True,
        figsize=(12, 6),
        color=colores[:len(cols_estado)]
    )
    plt.title('Casos COVID-19 por Municipio y Estado de Salud', fontsize=14, fontweight='bold')
    plt.xlabel('Municipio')
    plt.ylabel('Numero de Casos')
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='Estado', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(os.path.join(carpeta_evidencias, '4_municipios_por_estado.png'), bbox_inches='tight')
    plt.close()
    print("      Grafico de barras guardado en 'graficos/4_municipios_por_estado.png'.")

    # --- Grafico B: Heatmap de correlacion Municipio vs Estado ---
    # Se normaliza por fila (% dentro de cada municipio) para comparar proporciones
    tabla_norm = tabla[cols_estado].div(tabla['Total'], axis=0) * 100

    plt.figure(figsize=(10, max(4, len(tabla_norm) * 0.6 + 2)))
    sns.heatmap(
        tabla_norm,
        annot=True,
        fmt='.1f',
        cmap='YlOrRd',
        linewidths=0.5,
        linecolor='white',
        cbar_kws={'label': '% de casos en el municipio'}
    )
    plt.title('Distribucion (%) de Estados de Salud por Municipio\n(Heatmap de Correlacion)', 
              fontsize=13, fontweight='bold')
    plt.xlabel('Estado de Salud')
    plt.ylabel('Municipio')
    plt.xticks(rotation=30, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig(os.path.join(carpeta_evidencias, '5_heatmap_municipio_estado.png'), bbox_inches='tight')
    plt.close()
    print("      Heatmap guardado en 'graficos/5_heatmap_municipio_estado.png'.")

    return tabla


def generar_tabla_municipios_sin_manizales(df_crudo, base_dir):
    """
    Genera una tabla comparativa por municipio sin contar Manizales,
    mostrando cantidad y porcentaje de casos segun estado.
    Guarda CSV en 'datos_procesados/tabla_municipios_sin_manizales.csv'
    y un grafico de barras en 'graficos/9_municipios_sin_manizales.png'.
    """
    print("\n      [Tabla Comparativa] Casos por Municipio (Sin Manizales):")

    df = df_crudo.copy()
    df['Estado'] = df['Estado'].astype(str).str.strip()
    df['Nombre municipio'] = df['Nombre municipio'].astype(str).str.strip().str.upper()

    # Filtrar Manizales
    df = df[df['Nombre municipio'] != 'MANIZALES']

    # --- Tabla pivot: filas = municipio, columnas = estado ---
    tabla = df.pivot_table(
        index='Nombre municipio',
        columns='Estado',
        aggfunc='size',
        fill_value=0
    )

    # Orden de menor a mayor gravedad
    orden_real = ['Leve', 'Asintomático', 'Moderado', 'Grave', 'Fallecido']
    cols_estado = [c for c in orden_real if c in tabla.columns]
    tabla = tabla.reindex(columns=cols_estado, fill_value=0)

    # Total y porcentaje por municipio
    tabla['Total'] = tabla.sum(axis=1)
    for col in cols_estado:
        tabla[f'% {col}'] = (tabla[col] / tabla['Total'] * 100).round(1)

    print(tabla.to_string())

    # Guardar CSV
    ruta_procesados = os.path.join(base_dir, 'datos_procesados')
    os.makedirs(ruta_procesados, exist_ok=True)
    tabla.to_csv(os.path.join(ruta_procesados, 'tabla_municipios_sin_manizales.csv'))
    print("\n      Tabla sin Manizales guardada en 'datos_procesados/tabla_municipios_sin_manizales.csv'.")

    carpeta_evidencias = os.path.join(base_dir, 'graficos')
    os.makedirs(carpeta_evidencias, exist_ok=True)

    # --- Grafico: Barras apiladas por municipio sin Manizales ---
    colores = ['#2ecc71', '#a8e6cf', '#f39c12', '#e74c3c', '#7f0000']
    
    ax = tabla[cols_estado].plot(
        kind='bar',
        stacked=True,
        figsize=(12, 6),
        color=colores[:len(cols_estado)]
    )
    plt.title('Casos COVID-19 por Municipio (Excluyendo Manizales) y Estado de Salud', fontsize=14, fontweight='bold')
    plt.xlabel('Municipio')
    plt.ylabel('Numero de Casos')
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='Estado', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(os.path.join(carpeta_evidencias, '9_municipios_sin_manizales.png'), bbox_inches='tight')
    plt.close()
    print("      Grafico sin Manizales guardado en 'graficos/9_municipios_sin_manizales.png'.")

    return tabla


def generar_grafico_torta_edad(df_clean, base_dir):
    """
    Genera un grafico de torta de la distribucion de edad en tres intervalos:
    1 a 30 años, 31 a 60 años, y más de 60 años.
    Guarda CSV en 'datos_procesados/tabla_intervalos_edad.csv'
    y grafico en 'graficos/10_distribucion_edad_torta.png'.
    """
    print("\n      [Grafico de Torta] Distribucion de Casos por Intervalos de Edad:")
    
    df = df_clean.copy()
    df['Edad'] = pd.to_numeric(df['Edad'], errors='coerce')
    df = df.dropna(subset=['Edad'])

    # Crear intervalos
    bins = [0, 30, 60, float('inf')]
    labels = ['1 a 30 años', '31 a 60 años', 'Más de 60 años']
    df['Intervalo_Edad'] = pd.cut(df['Edad'], bins=bins, labels=labels)

    # Calcular frecuencias
    frec_abs = df['Intervalo_Edad'].value_counts()
    frec_rel = df['Intervalo_Edad'].value_counts(normalize=True) * 100
    
    tabla_edad = pd.DataFrame({
        'Intervalo de Edad': frec_abs.index,
        'Casos': frec_abs.values,
        'Porcentaje (%)': frec_rel.values.round(2)
    })
    
    # Reordenar según los intervalos lógicos
    tabla_edad['Intervalo de Edad'] = pd.Categorical(tabla_edad['Intervalo de Edad'], categories=labels, ordered=True)
    tabla_edad = tabla_edad.sort_values('Intervalo de Edad').reset_index(drop=True)
    
    print(tabla_edad.to_string(index=False))

    # Guardar CSV
    ruta_procesados = os.path.join(base_dir, 'datos_procesados')
    os.makedirs(ruta_procesados, exist_ok=True)
    tabla_edad.to_csv(os.path.join(ruta_procesados, 'tabla_intervalos_edad.csv'), index=False)
    print("\n      Tabla de intervalos de edad guardada en 'datos_procesados/tabla_intervalos_edad.csv'.")

    # --- Gráfico de Torta Premium ---
    plt.figure(figsize=(8, 8))
    colores_pie = ['#3498db', '#2ecc71', '#e74c3c']  # Azul suave, Verde suave, Rojo suave
    
    # Efecto premium de separación sutil y sombra
    explode = (0.02, 0.02, 0.05) 
    
    plt.pie(
        tabla_edad['Casos'],
        explode=explode,
        labels=tabla_edad['Intervalo de Edad'],
        autopct='%1.1f%%',
        startangle=140,
        colors=colores_pie,
        shadow=True,
        textprops={'fontsize': 12, 'fontweight': 'bold', 'color': '#2c3e50'}
    )
    
    plt.title('Distribucion Porcentual de Casos COVID-19 por Grupos de Edad\n(Caldas)', fontsize=14, fontweight='bold', pad=20)
    
    carpeta_evidencias = os.path.join(base_dir, 'graficos')
    os.makedirs(carpeta_evidencias, exist_ok=True)
    plt.savefig(os.path.join(carpeta_evidencias, '10_distribucion_edad_torta.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("      Grafico de torta guardado en 'graficos/10_distribucion_edad_torta.png'.")

    return tabla_edad


def generar_analisis_edad_estado(df_crudo, base_dir):
    """
    Analiza la relacion entre la Edad del paciente y su Estado de salud
    (Leve, Asintomatico, Moderado, Grave, Fallecido).
    Genera una tabla estadistica y tres graficos complementarios.
    """
    print("\n      [Analisis] Relacion Edad vs Estado del Paciente:")

    df = df_crudo.copy()
    df['Estado'] = df['Estado'].astype(str).str.strip()
    df['Edad']   = pd.to_numeric(df['Edad'], errors='coerce')
    df = df.dropna(subset=['Estado', 'Edad'])

    # Orden de gravedad para que los graficos sean legibles
    orden_estado = ['Leve', 'Asintom\u00e1tico', 'Moderado', 'Grave', 'Fallecido']
    estados_presentes = [e for e in orden_estado if e in df['Estado'].unique()]

    # --- Tabla estadistica: media, mediana, std, min, max por estado ---
    tabla_stats = df.groupby('Estado')['Edad'].agg(
        Media='mean',
        Mediana='median',
        Desv_Std='std',
        Minimo='min',
        Maximo='max',
        N='count'
    ).round(1)
    # Reordenar segun gravedad
    tabla_stats = tabla_stats.reindex([e for e in orden_estado if e in tabla_stats.index])
    print(tabla_stats.to_string())

    # Guardar tabla como CSV
    ruta_procesados = os.path.join(base_dir, 'datos_procesados')
    os.makedirs(ruta_procesados, exist_ok=True)
    tabla_stats.to_csv(os.path.join(ruta_procesados, 'estadisticas_edad_por_estado.csv'))
    print("\n      Tabla guardada en 'datos_procesados/estadisticas_edad_por_estado.csv'.")

    carpeta_evidencias = os.path.join(base_dir, 'graficos')
    os.makedirs(carpeta_evidencias, exist_ok=True)

    paleta = {'Leve': '#2ecc71', 'Asintom\u00e1tico': '#a8e6cf',
               'Moderado': '#f39c12', 'Grave': '#e74c3c', 'Fallecido': '#7f0000'}
    colores = [paleta.get(e, '#888888') for e in estados_presentes]

    # --- Grafico A: Boxplot Edad por Estado ---
    plt.figure(figsize=(10, 5))
    sns.boxplot(
        data=df[df['Estado'].isin(estados_presentes)],
        x='Estado', y='Edad',
        order=estados_presentes,
        palette=paleta
    )
    plt.title('Distribucion de Edad por Estado del Paciente (Boxplot)', fontsize=13, fontweight='bold')
    plt.xlabel('Estado de Salud')
    plt.ylabel('Edad (anos)')
    plt.xticks(rotation=20, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(carpeta_evidencias, '6_boxplot_edad_por_estado.png'), bbox_inches='tight')
    plt.close()
    print("      Boxplot guardado en 'graficos/6_boxplot_edad_por_estado.png'.")

    # --- Grafico B: Violin plot Edad por Estado ---
    plt.figure(figsize=(10, 5))
    sns.violinplot(
        data=df[df['Estado'].isin(estados_presentes)],
        x='Estado', y='Edad',
        order=estados_presentes,
        palette=paleta,
        inner='quartile'
    )
    plt.title('Densidad de Edad por Estado del Paciente (Violin)', fontsize=13, fontweight='bold')
    plt.xlabel('Estado de Salud')
    plt.ylabel('Edad (anos)')
    plt.xticks(rotation=20, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(carpeta_evidencias, '7_violin_edad_por_estado.png'), bbox_inches='tight')
    plt.close()
    print("      Violin plot guardado en 'graficos/7_violin_edad_por_estado.png'.")

    # --- Grafico C: Distribucion superpuesta (KDE) por Estado ---
    plt.figure(figsize=(10, 5))
    for estado, color in zip(estados_presentes, colores):
        subset = df[df['Estado'] == estado]['Edad']
        if len(subset) > 5:
            sns.kdeplot(subset, label=estado, color=color, fill=True, alpha=0.35, linewidth=1.5)
    plt.title('Distribucion de Edades por Estado (Densidad KDE)', fontsize=13, fontweight='bold')
    plt.xlabel('Edad (anos)')
    plt.ylabel('Densidad')
    plt.legend(title='Estado')
    plt.tight_layout()
    plt.savefig(os.path.join(carpeta_evidencias, '8_kde_edad_por_estado.png'), bbox_inches='tight')
    plt.close()
    print("      KDE guardado en 'graficos/8_kde_edad_por_estado.png'.")

    return tabla_stats

def ejecutar_analisis_exploratorio(df_clean, base_dir, df_crudo=None):
    """
    Recibe el DataFrame limpio y:
    - Genera tabla de frecuencias absolutas y relativas.
    - Imprime el resumen descriptivo de la Edad (cuartiles).
    - Guarda graficos: Countplot, Boxplot, Matriz de Correlacion numerica.
    - Si se provee df_crudo, genera tabla comparativa + heatmap Municipio vs Estado.
    """
    print("    Generando estadisticas y visualizaciones...")

    carpeta_evidencias = os.path.join(base_dir, 'graficos')
    os.makedirs(carpeta_evidencias, exist_ok=True)

    # 1. Resumen Estadistico (Cuartiles de Edad)
    print("\n      [Estadística] Cuartiles de Edad:")
    print(df_clean['Edad'].describe().to_string())

    # 2. Frecuencias del Target (Balance de clases)
    print("\n      [Estadística] Frecuencias de Gravedad (Target):")
    frecuencia_abs = df_clean['Target_Gravedad'].value_counts()
    frecuencia_rel = df_clean['Target_Gravedad'].value_counts(normalize=True) * 100
    tabla_frecuencias = pd.DataFrame({
        'Absoluta': frecuencia_abs,
        'Relativa (%)': frecuencia_rel.round(2)
    })
    tabla_frecuencias.index = ['Leve/Asintomatico (0)', 'Moderado/Grave/Fallecido (1)']
    print(tabla_frecuencias.to_string())

    # 3. Tabla comparativa + heatmap por municipio (requiere datos crudos)
    if df_crudo is not None:
        generar_tabla_municipios(df_crudo, base_dir)
        generar_tabla_municipios_sin_manizales(df_crudo, base_dir)
        generar_analisis_edad_estado(df_crudo, base_dir)

    # 4. Generacion de Graficos sobre df_clean

    sns.set_theme(style="whitegrid")

    # A. Distribucion del Target
    plt.figure(figsize=(6, 4))
    sns.countplot(data=df_clean, x='Target_Gravedad', palette='viridis')
    plt.title('Distribución de la Gravedad de los Casos')
    plt.xticks(ticks=[0, 1], labels=['Leve/Asint. (0)', 'Grave/Fall. (1)'])
    plt.tight_layout()
    plt.savefig(os.path.join(carpeta_evidencias, '1_distribucion_target.png'))
    plt.close()

    # B. Edad vs Gravedad (Boxplot)
    plt.figure(figsize=(8, 5))
    sns.boxplot(data=df_clean, x='Target_Gravedad', y='Edad', palette='Set2')
    plt.title('Distribución de Edad según Gravedad')
    plt.xticks(ticks=[0, 1], labels=['Leve/Asint. (0)', 'Grave/Fall. (1)'])
    plt.tight_layout()
    plt.savefig(os.path.join(carpeta_evidencias, '2_edad_vs_gravedad.png'))
    plt.close()

    # C. Matriz de Correlacion Numerica
    plt.figure(figsize=(8, 6))
    matriz_corr = df_clean.corr()
    sns.heatmap(matriz_corr, annot=True, cmap='coolwarm', fmt=".2f", vmin=-1, vmax=1)
    plt.title('Matriz de Correlación Numérica')
    plt.tight_layout()
    plt.savefig(os.path.join(carpeta_evidencias, '3_matriz_correlacion.png'))
    plt.close()

    generar_grafico_torta_edad(df_clean, base_dir)

    print(f"\n    EDA finalizado. Las evidencias visuales fueron guardadas en 'graficos/'.")

    return df_clean
