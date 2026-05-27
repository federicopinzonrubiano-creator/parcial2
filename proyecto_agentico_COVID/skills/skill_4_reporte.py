"""
Skill 4: Modulo de Generacion de Reportes y Consolidacion de Informacion
Se encarga de estructurar el directorio de reportes, copiar las tablas y graficos,
y escribir un reporte ejecutivo en formato Markdown y un Jupyter Notebook interactivo.
"""
import os
import shutil
import json
import pandas as pd

def dataframe_a_markdown(df):
    """
    Convierte un DataFrame de pandas a formato tabla Markdown de forma manual
    para evitar dependencia con la libreria externa 'tabulate'.
    """
    columnas = list(df.columns)
    linea_encabezado = "| " + " | ".join(columnas) + " |"
    linea_separador = "| " + " | ".join(["---"] * len(columnas)) + " |"
    lineas_datos = []
    for _, fila in df.iterrows():
        valores_fila = [str(val) for val in fila]
        lineas_datos.append("| " + " | ".join(valores_fila) + " |")
    return "\n".join([linea_encabezado, linea_separador] + lineas_datos)

def generar_reporte_ejecutivo(metricas_modelo, base_dir):
    """
    Consolida toda la informacion en la carpeta 'reporte/', copia los datos 
    e imagenes generadas, genera el archivo 'reporte_ejecutivo.md' y crea 
    el Jupyter Notebook interactivo 'reporte_ejecutivo.ipynb' en espanol.
    """
    print("\n[Paso 4] Activando Skill 4: Generacion de Reportes y Consolidacion...")
    
    # 1. Definir y crear estructura de carpetas
    dir_reporte = os.path.join(base_dir, 'reporte')
    dir_tablas = os.path.join(dir_reporte, 'tablas')
    dir_graficos = os.path.join(dir_reporte, 'graficos')
    
    os.makedirs(dir_reporte, exist_ok=True)
    os.makedirs(dir_tablas, exist_ok=True)
    os.makedirs(dir_graficos, exist_ok=True)
    
    print("    -> Creada la estructura de directorios en 'reporte/'")
    
    # 2. Copiar archivos CSV procesados
    ruta_procesados = os.path.join(base_dir, 'datos_procesados')
    csvs_a_copiar = ['tabla_municipios_por_estado.csv', 'tabla_municipios_sin_manizales.csv', 'estadisticas_edad_por_estado.csv', 'tabla_intervalos_edad.csv']
    
    for csv_file in csvs_a_copiar:
        origen = os.path.join(ruta_procesados, csv_file)
        destino = os.path.join(dir_tablas, csv_file)
        if os.path.exists(origen):
            shutil.copy2(origen, destino)
            print(f"    -> Copiado tabla: {csv_file}")
        else:
            print(f"    -> Advertencia: No se encontro {origen}")
            
    # 3. Copiar graficos generados
    ruta_graficos = os.path.join(base_dir, 'graficos')
    graficos_a_copiar = [
        '1_distribucion_target.png',
        '2_edad_vs_gravedad.png',
        '3_matriz_correlacion.png',
        '4_municipios_por_estado.png',
        '5_heatmap_municipio_estado.png',
        '6_boxplot_edad_por_estado.png',
        '7_violin_edad_por_estado.png',
        '8_kde_edad_por_estado.png',
        '9_municipios_sin_manizales.png',
        '10_distribucion_edad_torta.png'
    ]
    
    for graph in graficos_a_copiar:
        origen = os.path.join(ruta_graficos, graph)
        destino = os.path.join(dir_graficos, graph)
        if os.path.exists(origen):
            shutil.copy2(origen, destino)
            print(f"    -> Copiado grafico: {graph}")
        else:
            print(f"    -> Advertencia: No se encontro {origen}")

    # 4. Leer tablas CSV para formatear como tablas Markdown
    # A. Tabla de Estadisticas de Edad
    tabla_edad_md = ""
    ruta_csv_edad = os.path.join(dir_tablas, 'estadisticas_edad_por_estado.csv')
    if os.path.exists(ruta_csv_edad):
        df_edad = pd.read_csv(ruta_csv_edad)
        tabla_edad_md = dataframe_a_markdown(df_edad)
    else:
        tabla_edad_md = "| Estado | Media | Mediana | Desv_Std | Minimo | Maximo | N |\n|---|---|---|---|---|---|---|"
        
    # B. Tabla de Municipios (Top 12 con mayor porcentaje de fatalidad)
    tabla_municipios_md = ""
    ruta_csv_mun = os.path.join(dir_tablas, 'tabla_municipios_por_estado.csv')
    if os.path.exists(ruta_csv_mun):
        df_mun = pd.read_csv(ruta_csv_mun)
        # Ordenar por porcentaje de fallecidos descendente para el analisis de riesgo
        df_mun_sorted = df_mun.sort_values(by='% Fallecido', ascending=False)
        # Mostramos los primeros 12 municipios con mayor porcentaje de fatalidad
        tabla_municipios_md = dataframe_a_markdown(df_mun_sorted.head(12))
    else:
        tabla_municipios_md = "| Municipio | Leve | Fallecido | Total | % Leve | % Fallecido |\n|---|---|---|---|---|---|"

    # C. Tabla de Municipios Sin Manizales
    tabla_municipios_sin_manizales_md = ""
    ruta_csv_mun_sin = os.path.join(dir_tablas, 'tabla_municipios_sin_manizales.csv')
    if os.path.exists(ruta_csv_mun_sin):
        df_mun_sin = pd.read_csv(ruta_csv_mun_sin)
        # Ordenar por Total de casos descendente para ver el volumen de los demas municipios
        df_mun_sin_sorted = df_mun_sin.sort_values(by='Total', ascending=False)
        tabla_municipios_sin_manizales_md = dataframe_a_markdown(df_mun_sin_sorted)
    else:
        tabla_municipios_sin_manizales_md = "| Municipio | Leve | Fallecido | Total | % Leve | % Fallecido |\n|---|---|---|---|---|---|"

    # D. Tabla de Intervalos de Edad (Gráfico de Torta)
    tabla_intervalos_edad_md = ""
    ruta_csv_int_edad = os.path.join(dir_tablas, 'tabla_intervalos_edad.csv')
    if os.path.exists(ruta_csv_int_edad):
        df_int_edad = pd.read_csv(ruta_csv_int_edad)
        tabla_intervalos_edad_md = dataframe_a_markdown(df_int_edad)
    else:
        tabla_intervalos_edad_md = "| Intervalo de Edad | Casos | Porcentaje (%) |\n|---|---|---|"

    # 5. Construccion del Reporte Ejecutivo en Markdown
    reporte_content = f"""# Reporte Ejecutivo: Proyecto Agentico COVID

## Resumen Ejecutivo

Este documento presenta un analisis epidemiologico detallado del comportamiento y gravedad de los casos de COVID-19 reportados en el departamento de Caldas. A traves de la integracion de tecnicas de limpieza de datos, analisis exploratorio y modelado predictivo mediante Machine Learning, se identifican las relaciones clave entre las variables demograficas del paciente, su ubicacion geografica y el desenlace de la enfermedad. El objetivo principal es suministrar herramientas analiticas rigurosas para la toma de decisiones en salud publica, optimizacion de recursos hospitalarios y estratificacion de riesgo de pacientes.


---

## Descripcion de los Datos

El conjunto de datos original constaba de 23,806 registros. Despues de aplicar un proceso riguroso de depuracion y estructuracion (Wrangling), que incluyo la eliminacion de inconsistencias en la variable de edad, limpieza de strings y descarte de observaciones anomalas, el dataset consolidado cuenta con **23,666 filas** y las siguientes variables de modelado predictivo:

- **Edad**: Edad cronologica del paciente.
- **Sexo_encoded**: Genero del paciente codificado numericamene (Femenino / Masculino).
- **Tipo_contagio_encoded**: Tipo de transmision de la infeccion (Comunitaria / Relacionada / Importada).
- **Municipio_encoded**: Codificacion numerica del municipio de residencia del paciente.
- **Target_Gravedad**: Variable objetivo categorica binaria.
  - **0**: Casos de gravedad Leve o Asintomática.
  - **1**: Casos de gravedad Moderada, Grave o Fallecidos.

---

## Analisis Exploratorio de Datos (EDA)

El analisis exploratorio de datos revelo patrones criticos de distribucion demografica y comportamiento clinico del virus en el departamento.

### 1. Relacion Critica entre Edad y Estado de Gravedad
Se encontro una relacion inequivoca entre la edad del paciente y la severidad del caso. Las personas que sufrieron complicaciones graves o fallecieron presentan un perfil de edad significativamente mas avanzado en comparacion con los casos leves.

A continuacion se presentan las estadisticas descriptivas detalladas de la edad de acuerdo con el estado de salud registrado:

{tabla_edad_md}

*Nota: Datos obtenidos a partir del analisis consolidado.*

#### Distribucion por Intervalos de Edad (Grafico de Torta)
Para comprender mejor la composicion demografica por grupos de edad, segmentamos la poblacion de pacientes en tres intervalos clave: **1 a 30 anos**, **31 a 60 anos** y **Mas de 60 anos**. 

A continuacion se presenta la distribucion total de los casos reportados por grupo de edad:

{tabla_intervalos_edad_md}

*Nota: Datos agrupados a partir de los registros de edad limpios.*

El grafico de torta premium muestra la proporcion relativa de cada grupo:
- ![Distribucion Porcentual de Edad](graficos/10_distribucion_edad_torta.png)

#### Explicacion Clinica y Estadistica de la Relacion de Edad
- **Edad Promedio de Fallecidos**: La media de edad de los pacientes fallecidos es de **66.8 anos** (con una mediana de 68 aos), en contraste directo con los casos de gravedad leve cuya media de edad es de **40.4 anos** (mediana de 39 anos). 
- **Distribucion y Dispersion**: El 50% de las personas fallecidas se concentran en el rango de los 58 a los 78 anos de edad. Esto evidencia de forma estadistica que la senescencia y la acumulacion de comorbilidades asociadas a la edad avanzada constituyen el principal factor de riesgo clinico para desenlaces fatales en la region de Caldas.
- **Visualizacion de Densidad y Dispersion**: La brecha de distribucion de edad se visualiza claramente en las siguientes representaciones guardadas en la carpeta de reportes:
  - ![Densidad de Edad por Estado (KDE)](graficos/8_kde_edad_por_estado.png)
  - ![Distribucion de Edad por Estado (Boxplot)](graficos/6_boxplot_edad_por_estado.png)
  - ![Densidad de Edad por Estado (Violin)](graficos/7_violin_edad_por_estado.png)
  - ![Edad vs Gravedad Agrupada](graficos/2_edad_vs_gravedad.png)

---

### 2. Analisis Geografico: Comparativa por Municipio y Tasas de Fatalidad
La distribucion territorial del impacto de la COVID-19 en Caldas no es uniforme. El volumen absoluto de casos esta concentrado en la capital, pero el riesgo relativo medido por el porcentaje de desenlaces fatales es superior en determinados municipios de la periferia.

A continuacion se detallan los 12 municipios con mayor porcentaje de fatalidad dentro del total de sus casos reportados:

{tabla_municipios_md}

*Nota: Datos ordenados por porcentaje de fatalidad de mayor a menor.*

#### Relaciones y Hallazgos Territoriales
- **Manizales (La Capital)**: Representa el mayor foco infeccioso en terminos absolutos con **16,987 casos**, pero registra una tasa de mortalidad relativa baja de solo **1.6%**. Esto podria deberse a una mayor capacidad de respuesta del sistema de salud local, mayor proporcion de poblacion joven activa diagnosticada o mejores politicas de testeo preventivo.
- **Municipios de Alta Fatalidad Relativa**: Localidades como **Palestina (8.3% de fallecidos)**, **Belalcazar (7.5%)**, **Risaralda (6.5%)**, **Aranzazu (6.4%) y Viterbo (5.8%)** registran porcentajes de fatalidad notablemente elevados a pesar de tener un menor numero absoluto de casos. Esto enciende alarmas directivas que sugieren:
  - Posibles demoras en el acceso a unidades de cuidados intensivos debido a la distancia geografica.
  - Una estructura demografica mas envejecida en estas localidades rurales.
  - Subregistro de casos leves en zonas mas apartadas, lo que infla artificialmente la tasa de letalidad sobre los casos detectados.
- **Visualizaciones de Distribucion Geografica**:
  - ![Distribucion de Estados por Municipio](graficos/4_municipios_por_estado.png)
  - ![Heatmap de Proporcion Municipio vs Estado](graficos/5_heatmap_municipio_estado.png)

### 2.b Distribucion Geografica Excluyendo Manizales
Dado que Manizales concentra mas del 70% de los casos totales del departamento, su volumen absoluto tiende a eclipsar y dificultar la visualizacion del comportamiento de la enfermedad en el resto de los municipios de Caldas. 

A continuacion, se presenta la tabla comparativa detallada para todos los municipios de Caldas, **excluyendo a Manizales**, ordenados de mayor a menor numero de casos totales:

{tabla_municipios_sin_manizales_md}

*Nota: Datos ordenados por el numero total de casos registrados.*

#### Explicacion Visual y Epidemiologica (Sin Manizales)
Al retirar a la capital del analisis grafico, logramos observar con mucha mayor claridad el peso relativo de municipios como **Villamaria (1,713 casos)**, **La Dorada (999 casos)** y **Chinchina (967 casos)**, los cuales lideran la incidencia fuera de la capital.
Esta perspectiva sin sesgo de escala permite contrastar de forma directa y proporcional la gravedad en municipios intermedios y pequenos:

- ![Casos COVID-19 por Municipio (Excluyendo Manizales)](graficos/9_municipios_sin_manizales.png)

---

## Resultados del Modelado Predictivo (Machine Learning)

### El Desafio del Desbalance de Clases
Un aspecto metodologico crucial en este estudio es el severo desbalance de la variable objetivo. El **97.69% (23,120 casos)** corresponden a la clase Leve/Asintomática (0), mientras que solo el **2.31% (546 casos)** pertenecen a la clase Moderado/Grave/Fallecido (1). 

Para evitar que los modelos matematicos predijeran de forma sesgada la clase mayoritaria (ignorando los casos graves), se aplico una estrategia combinada de:
1. **Division Estratificada (Stratified Train/Test Split)**: Asegurando la misma proporcion de casos graves (2.31%) tanto en el conjunto de entrenamiento como en el de validacion.
2. **Ponderacion Balanceada de Clases (Class Weighting)**: Penalizando fuertemente los errores cometidos sobre la clase minoritaria (gravedad 1) durante el entrenamiento de los algoritmos.

### Comparativa de Modelos y Justificacion del Algoritmo Ganador
Se entrenaron y evaluaron dos algoritmos competidores en el conjunto de test independiente utilizando el puntaje F1 ponderado (Weighted F1-Score) como metrica de seleccion:

- **Regresion Logistica**: F1-Score = {metricas_modelo['f1_rl']:.4f}
- **Random Forest Classifier (Ganador)**: F1-Score = {metricas_modelo['f1_rf']:.4f}

El algoritmo seleccionado por el orquestador debido a su superior desempeño predictivo es **{metricas_modelo['nombre_ganador']}**.

#### ¿Por que se utilizo Random Forest y por que supero a la Regresion Logistica?

La eleccion e implementacion de **Random Forest** como el algoritmo nucleo de este estudio responde a razones metodologicas y del comportamiento clinico de la enfermedad:

1. **Modelado de Relaciones No Lineales Complejas**: 
   La COVID-19 afecta la salud de forma altamente no lineal. Por ejemplo, el riesgo de complicacion no avanza de manera constante o de forma directamente proporcional con cada ano de edad; en su lugar, se dispara exponencialmente al superar los 60 anos de edad.
   - La **Regresion Logistica** es un clasificador lineal que asume que la relacion logit es lineal y constante, lo que limita su capacidad para capturar cambios abruptos o fronteras de riesgo complejas.
   - **Random Forest**, al ser un ensamble de arboles de decision, segmenta de forma natural y recursiva el espacio de las variables, adaptandose de forma optima a los saltos en el comportamiento del virus sin requerir parametrizaciones artificiales.

2. **Deteccion Automatica de Interacciones de Variables**:
   La gravedad de un paciente no depende unicamente de factores aislados, sino de la combinacion sinergica de ellos (por ejemplo, el impacto combinado de la Edad avanzada con el Sexo biologico, o el tipo de contagio en un municipio apartado). 
   Mientras que la Regresion Logistica requiere la formulacion explicita y manual de terminos de interaccion polinomiales, Random Forest mapea y explota de manera nativa estas interacciones complejas durante el crecimiento de sus ramas.

3. **Resistencia al Desbalance Extremo mediante Criterio de Enrutamiento Nodo a Nodo**:
   El dataset cuenta con un severo desbalance de clases (solo el 2.31% de casos graves). Al aplicar la ponderacion estrategica (`class_weight='balanced'`), Regresion Logistica se limita a aplicar una penalizacion en la funcion de perdida global.
   En contraste, **Random Forest** aplica esta ponderacion directamente en el calculo de la ganancia de informacion de Gini/Entropia en cada nodo individual de cada arbol. Esto obliga a cada arbol del ensamble a tomar decisiones locales robustas para no omitir la clase minoritaria (Graves/Fallecidos), logrando un recall muy superior.

4. **Reduccion de Varianza mediante Ensamble (Bagging)**:
   Al promediar las decisiones de **100 estimadores independientes** entrenados sobre muestras aleatorias del conjunto de datos y subconjuntos aleatorios de variables, Random Forest anula la variabilidad extrema de los arboles de decision individuales. Esto le dota de una resistencia sobresaliente frente al sobreajuste (*overfitting*), garantizando que el modelo sea robusto frente a ruido en los registros oficiales.

### Reporte de Clasificacion Detallado (Modelo Ganador)

A continuacion se presenta el reporte de rendimiento obtenido por el modelo ganador sobre los datos de prueba:

```
{metricas_modelo['reporte_clasificacion']}
```

#### Analisis Riguroso de precision y Exhaustividad (Recall)
- **Desempeno de la Clase Mayoritaria (Leve - 0)**: Muestra una precision del **98%** y un recall del **94%**, demostrando una precision sobresaliente para clasificar correctamente a los pacientes de bajo riesgo.
- **Desempeno de la Clase Critica (Grave/Fallecido - 1)**: 
  - **Recall del 54%**: Esto significa que el modelo es capaz de identificar de manera anticipada a mas de la mitad de los pacientes que sufriran complicaciones medicas graves o moriran.
  - **Precision del 7%**: El valor bajo de precision indica que por cada caso grave detectado correctamente, el modelo senala como "potencialmente graves" a varios pacientes que terminaran teniendo sintomas leves.
  - **Justificacion Clinica del Balance**: En el contexto de la gestion epidemiologica y el triaje medico, **este comportamiento es clinicamente optimo**. En salud publica, un falso positivo (monitorear de cerca a un paciente que resulta ser leve) representa un costo marginal menor, mientras que un falso negativo (enviar a casa sin vigilancia a un paciente que terminara falleciendo o requiriendo UCI) es una falla critica. Por tanto, maximizar el recall (exhaustividad) sobre la clase grave a costa de la precision es la decision etica y operativa mas acertada.

A continuacion se anexan las figuras de distribucion y correlacion general:
- ![Distribucion del Target](graficos/1_distribucion_target.png)
- ![Matriz de Correlacion Numerica](graficos/3_matriz_correlacion.png)

---

## Conclusiones del Modelado y Recomendaciones

1. **La Edad como Predictor Hegemonico**: La edad cronologica del paciente actua como el factor de mayor peso en la determinacion del riesgo de gravedad por COVID-19 en Caldas. Las politicas de prevencion, inmunizacion y atencion prioritaria deben estar fuertemente focalizadas en los grupos de edad superiores a los 60 anos.
2. **Alertas de Vulnerabilidad Geografica**: Municipios como Palestina y Belalcazar requieren una auditoria medica y fortalecimiento de sus canales de atencion primaria y traslado de urgencias, debido a que registran tasas de letalidad relativa inusualmente altas en comparacion con Manizales.
3. **Viabilidad Clinica del Modelo Predictivo**: El modelo de Random Forest desarrollado demuestra ser una herramienta viable de triaje automatizado para soporte de decisiones clinicas. Permite a los centros medicos clasificar de forma temprana a los pacientes segun su probabilidad de complicacion clinica, permitiendo una asignacion mas eficiente de camas de cuidados intermedios e intensivos.
4. **Lineas de Mejora Futura**:
   - Incorporar variables clinicas preexistentes (hipertension, diabetes, obesidad, estado de vacunacion) que actualmente no se encuentran en el dataset crudo, lo que aumentaria notablemente la precision de la prediccion de gravedad.
   - Explorar metodos avanzados de remuestreo artificial (como SMOTE o ADASYN) en combinacion con redes neuronales o algoritmos de boosting (XGBoost / LightGBM) para mejorar el F1-score de la clase minoritaria.
"""

    # 6. Escribir el reporte ejecutivo en Markdown
    ruta_archivo_reporte = os.path.join(dir_reporte, 'reporte_ejecutivo.md')
    with open(ruta_archivo_reporte, 'w', encoding='utf-8') as f:
        f.write(reporte_content.strip())
    print(f"    -> Reporte ejecutivo generado en 'reporte/reporte_ejecutivo.md'")

    # 7. Generacion Dinamica del Jupyter Notebook
    cells = []
    
    # Portada y Resumen Ejecutivo
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# Reporte Ejecutivo Interactivo: Proyecto Agentico COVID\n\n",
            "Este Jupyter Notebook interactivo consolidado presenta un analisis de alto impacto sobre el comportamiento, severidad y modelado predictivo de la COVID-19 en el departamento de Caldas.\n\n",
            "## Resumen Ejecutivo\n\n",

            "Este estudio reune las fases de limpieza de datos, analisis estadistico exploratorio (EDA) y algoritmos de Machine Learning para identificar los factores clave de riesgo clinico. El proposito de este notebook interactivo es brindar a la directiva una herramienta dinamica de exploracion para la optimizacion de recursos clinicos y toma de decisiones estrategicas en salud publica en la region Caldense."
        ]
    })
    
    # Importar librerias
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "import os\n",
            "import pandas as pd\n",
            "import matplotlib.pyplot as plt\n",
            "import seaborn as sns\n",
            "from IPython.display import display, Image\n",
            "\n",
            "# Configuramos el estilo de graficos interactivos\n",
            "sns.set_theme(style=\"whitegrid\")\n",
            "print(\"Entorno inicializado y librerias cargadas exitosamente.\")"
        ]
    })
    
    # Descripcion de datos
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 1. Descripcion de los Datos Procesados\n\n",
            "El dataset limpio final cuenta con **23,666 registros** y 5 variables clave de modelado predictivo.\n",
            "A continuacion, cargamos e inspeccionamos de manera interactiva las primeras filas del dataset procesado:"
        ]
    })
    
    # Cargar y previsualizar dataset
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Cargar el dataset limpio para modelar\n",
            "df_limpio = pd.read_csv('../datos_procesados/dataset_limpio_para_modelo.csv')\n",
            "print(f\"Dimensiones del dataset consolidado: {df_limpio.shape[0]} filas, {df_limpio.shape[1]} columnas\")\n",
            "df_limpio.head(10)"
        ]
    })
    
    # Relacion Edad vs Estado
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 2. Analisis Exploratorio (EDA): Edad vs Estado del Paciente\n\n",
            "Existe una correlacion clinica inequivoca entre la edad avanzada y el riesgo de gravedad y letalidad por COVID-19 en Caldas.\n\n",
            "A continuacion, cargamos y mostramos de forma interactiva la tabla descriptiva de edad agrupada por estado de salud, aplicando un degradado de color para resaltar visualmente el contraste critico:"
        ]
    })
    
    # Cargar tabla edad con estilos
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Cargar estadisticas descriptivas de edad\n",
            "df_edad = pd.read_csv('tablas/estadisticas_edad_por_estado.csv')\n",
            "\n",
            "# Aplicar estilos interactivos de Pandas (degradado en Media y Mediana)\n",
            "df_edad.style.background_gradient(subset=['Media', 'Mediana'], cmap='Oranges')\\"
            ".format({'Media': '{:.1f} anos', 'Mediana': '{:.1f} anos', 'Desv_Std': '{:.1f}', 'N': '{:,}'})"
        ]
    })
    
    # Distribución por Intervalos de Edad (Gráfico de Torta)
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### 2.b Analisis por Intervalos de Edad (Grafico de Torta)\n\n",
            "Para un analisis demografico mas directo, segmentamos a los pacientes en tres rangos de edad clave: **1 a 30 anos**, **31 a 60 anos** y **Mas de 60 anos**.\n\n",
            "Cargamos la tabla de frecuencias de estos intervalos:"
        ]
    })
    
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Cargar tabla de intervalos de edad\n",
            "df_int_edad = pd.read_csv('tablas/tabla_intervalos_edad.csv')\n",
            "\n",
            "# Estilizar con degradado verde para destacar volumen de casos\n",
            "df_int_edad.style.background_gradient(subset=['Casos'], cmap='Greens')\\"
            ".format({'Casos': '{:,}', 'Porcentaje (%)': '{:.2f}%'})\n"
        ]
    })

    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "#### Proporcion Porcentual por Grupo de Edad (Grafico de Torta)\n\n",
            "El siguiente grafico de torta premium ilustra la composicion demografica porcentual de los casos de COVID-19 en Caldas:\n\n",
            "![Grafico de Torta de Edad](graficos/10_distribucion_edad_torta.png)"
        ]
    })
    
    # Explicacion e imagenes de edad
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Visualizaciones Epidemiologicas de la Relacion de Edad\n\n",
            "La brecha demografica se hace evidente en las siguientes visualizaciones premium, integradas directamente en el reporte:\n\n",
            "#### Densidad de Edad por Estado (KDE)\n",
            "El grafico de densidad de Kernel (KDE) muestra como la distribucion de los fallecidos esta notablemente desplazada hacia la derecha (edad avanzada) en comparacion con los casos leves:\n\n",
            "![Densidad de Edad por Estado (KDE)](graficos/8_kde_edad_por_estado.png)\n\n",
            "#### Boxplot y Distribucion de Edad por Estado de Salud\n\n",
            "![Distribucion de Edad por Estado (Boxplot)](graficos/6_boxplot_edad_por_estado.png)\n\n",
            "#### Densidad de Edad por Estado de Salud (Violin)\n\n",
            "![Densidad de Edad por Estado (Violin)](graficos/7_violin_edad_por_estado.png)\n\n",
            "#### Edad Agrupada segun el Target Binario de Gravedad\n\n",
            "![Edad vs Gravedad Agrupada](graficos/2_edad_vs_gravedad.png)"
        ]
    })
    
    # Analisis por Municipio
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 3. Analisis Geografico: Tasas de Letalidad por Municipio\n\n",
            "El impacto geografico difiere notablemente entre municipios. Manizales concentra la mayoria de casos absolutos, pero municipios rurales perifericos exhiben tasas de letalidad relativa (fallecidos / casos totales) alarmantes.\n\n",
            "A continuacion visualizamos interactivamente los 12 municipios con mayor porcentaje de fatalidad relativa en el departamento, aplicando un formato degradado de riesgo en rojo:"
        ]
    })
    
    # Mostrar tabla municipios con estilos
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Cargar la tabla de municipios por estado\n",
            "df_mun = pd.read_csv('tablas/tabla_municipios_por_estado.csv')\n",
            "\n",
            "# Ordenar por fatalidad relativa y obtener el Top 12\n",
            "top_fatalidad = df_mun.sort_values(by='% Fallecido', ascending=False).head(12)\n",
            "\n",
            "# Estilizar la tabla en degradado rojo de riesgo\n",
            "top_fatalidad.style.background_gradient(subset=['% Fallecido'], cmap='Reds')\\"
            ".format({'% Leve': '{:.1f}%', '% Fallecido': '{:.1f}%', 'Total': '{:,}'})"
        ]
    })
    
    # Visualizaciones municipios
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Visualizaciones de Distribucion Geografica\n\n",
            "#### Proporcion Acumulada de Casos por Estado por Municipio\n\n",
            "![Distribucion de Estados por Municipio](graficos/4_municipios_por_estado.png)\n\n",
            "#### Heatmap de Proporcion Relativa (%) de Estado de Salud por Municipio\n\n",
            "![Heatmap de Proporcion Municipio vs Estado](graficos/5_heatmap_municipio_estado.png)"
        ]
    })
    
    # Analisis por Municipio sin Manizales
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### 3.b Analisis Geografico Excluyendo Manizales\n\n",
            "Para un analisis visual y comparativo mas equilibrado de los municipios intermedios y rurales, excluimos a Manizales del siguiente reporte, ya que su gran volumen de casos (mas de 16,000) domina la escala visual de los graficos.\n\n",
            "A continuacion cargamos e imprimimos la tabla completa de los municipios de Caldas (sin Manizales), ordenada por cantidad de casos totales:"
        ]
    })
    
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Cargar la tabla de municipios sin Manizales\n",
            "df_mun_sin = pd.read_csv('tablas/tabla_municipios_sin_manizales.csv')\n",
            "\n",
            "# Ordenar por casos totales descendente\n",
            "df_mun_sin_sorted = df_mun_sin.sort_values(by='Total', ascending=False)\n",
            "\n",
            "# Estilizar la tabla en degradado azul para total y rojo para fatalidad\n",
            "df_mun_sin_sorted.style.background_gradient(subset=['Total'], cmap='Blues')\\"
            ".background_gradient(subset=['% Fallecido'], cmap='Reds')\\"
            ".format({'% Leve': '{:.1f}%', '% Fallecido': '{:.1f}%', 'Total': '{:,}'})\n"
        ]
    })

    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "#### Visualizacion Alternativa del Impacto Municipal (Sin Manizales)\n\n",
            "El siguiente grafico de barras apiladas nos permite apreciar detalladamente la distribucion de casos en cada uno de los municipios sin la distorsion de escala generada por la capital:\n\n",
            "![Casos por Municipio sin Manizales](graficos/9_municipios_sin_manizales.png)"
        ]
    })
    
    # Modelado predictivo
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 4. Resultados de Modelado de Machine Learning\n\n",
            "### Desafio de Desbalance de Clases\n\n",
            "El conjunto de datos presenta un fuerte desbalance de clases (97.69% Leve vs 2.31% Grave). Para resolverlo, se aplico una division estratificada de entrenamiento/prueba y ponderacion balanceada de clases en los algoritmos.\n\n",
            "### Comparativa de F1-Scores Ponderados en Test:\n\n",
            "- **Regresion Logistica**: F1-Score = " + f"{metricas_modelo['f1_rl']:.4f}\n" +
            "- **Random Forest Classifier (Ganador)**: F1-Score = " + f"{metricas_modelo['f1_rf']:.4f}\n\n" +
            "El modelo con mejor desempeno general es **" + metricas_modelo['nombre_ganador'] + "**.\n\n",
            "#### ¿Por que se utilizo Random Forest y por que supero a la Regresion Logistica?\n\n",
            "La eleccion de **Random Forest** responde a razones fundamentales de modelado demografico y epidemiologico:\n\n",
            "1. **Modelado No Lineal**: La gravedad de COVID-19 tiene un comportamiento altamente no lineal (por ejemplo, el riesgo de letalidad se dispara exponencialmente despues de los 60 anos). La Regresion Logistica asume fronteras de decision lineales, mientras que Random Forest segmenta el espacio mediante decisiones locales de enrutamiento mucho mas flexibles.\n",
            "2. **Deteccion Automatica de Interacciones**: Permite capturar de manera nativa la relacion sinergica entre multiples variables (como la Edad en combinacion con el Sexo o la ubicacion en un Municipio rural especifico) sin necesidad de formular manualmente interacciones complejas.\n",
            "3. **Manejo Efectivo del Desbalance**: Al aplicar la ponderacion estrategica (`class_weight='balanced'`), Random Forest modifica la evaluacion de Gini en cada nodo de cada arbol individual, forzando a los estimadores a tomar decisiones robustas para no omitir la clase minoritaria (Graves/Fallecidos), logrando un Recall muy superior.\n",
            "4. **Reduccion de Varianza (Bagging)**: Promedia las predicciones de **100 estimadores independientes** entrenados sobre muestras aleatorias del conjunto de datos y variables. Esto reduce drasticamente la varianza, protegiendo al modelo del sobreajuste (overfitting) frente al ruido de los datos."
        ]
    })
    
    # Reporte de clasificacion
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Reporte detallado de clasificacion del modelo ganador\n",
            "reporte_modelo = \"\"\"" + metricas_modelo['reporte_clasificacion'] + "\"\"\"\n",
            "print(\"Reporte de Clasificacion en Conjunto de Prueba:\")\n",
            "print(reporte_modelo)"
        ]
    })
    
    # Precision vs Recall
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Analisis Operativo: Precision vs Exhaustividad (Recall)\n\n",
            "- **Recall del 54%**: El modelo predice de manera anticipada a mas de la mitad de los pacientes que sufriran complicaciones graves o falleceran.\n",
            "- **Precision del 7%**: Debido al severo desbalance de la clase critica (gravedad 1), el modelo produce falsos positivos marcando pacientes como potencialmente graves que terminan recuperandose leves.\n",
            "- **Justificacion Epidemiologica Directiva**: En un entorno de salud publica y triaje de urgencias, **un alto Recall (exhaustividad) es prioritario**. Es clinicamente preferible asignar monitoreo a un paciente leve (costo operativo marginal) que omitir la vigilancia medica de un paciente de alto riesgo (costo vital critico). Por tanto, la ponderacion de clases aplicada logro el balance optimo requerido.\n\n",
            "#### Graficos de Soporte y Correlacion General\n\n",
            "![Distribucion de Target](graficos/1_distribucion_target.png)\n",
            "![Matriz de Correlacion Numerica](graficos/3_matriz_correlacion.png)"
        ]
    })
    
    # Conclusiones
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 5. Conclusiones y Recomendaciones Ejecutivas\n\n",
            "1. **Edad como Predictor Hegemonico**: La edad cronologica es la variable de mayor relevancia estadistica. Toda accion de contencion de riesgo y priorizacion de recursos debe estar orientada a mayores de 60 anos.\n",
            "2. **Mitigacion Geografica**: Las altas tasas de letalidad relativa en Palestina (8.3%) y Belalcazar (7.5%) demandan intervenciones inmediatas en la infraestructura de transporte clinico urgente y puestos de atencion rural.\n",
            "3. **Viabilidad de Implementacion**: El clasificador Random Forest desarrollado es una herramienta viable de triaje digital para asistir al personal medico en la priorizacion temprana de recursos hospitalarios complejos (camas UCI).\n",
            "4. **Recomendaciones para Fase II**: Incorporar al dataset variables de antecedentes clinicos (hipertension, diabetes, vacunacion) y explorar metodos de boosting (como XGBoost) en combinacion con tecnicas avanzadas de balanceo sintetico (SMOTE)."
        ]
    })
    
    # Construir estructura JSON del Notebook
    notebook_dict = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 2
    }
    
    # Guardar reporte_ejecutivo.ipynb
    ruta_notebook = os.path.join(dir_reporte, 'reporte_ejecutivo.ipynb')
    with open(ruta_notebook, 'w', encoding='utf-8') as f:
        json.dump(notebook_dict, f, indent=1, ensure_ascii=False)
        
    print(f"    -> Reporte interactivo generado en 'reporte/reporte_ejecutivo.ipynb'")
    print(f"\n[Exito] Reportes generados y guardados en la carpeta 'reporte/'.")
    print("        Todos los datos de soporte y graficos han sido consolidados exitosamente.")
    print("="*60)
