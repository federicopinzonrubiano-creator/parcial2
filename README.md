# Proyecto de Análisis: Calidad del Vino (Wine Quality)

Este proyecto abarca el ciclo completo de análisis de datos para un conjunto de registros de la calidad del vino (blanco y tinto). El flujo va desde la recolección de los datos crudos, pasando por su limpieza (Data Wrangling), hasta llegar a un análisis exploratorio (EDA) exhaustivo que desentraña las diferencias químicas y su relación con la calidad.

## 1. Estructura del Proyecto

* `datos/crudos/`: Datos originales e inmutables (`winequality-red.csv` y `winequality-white.csv`).
* `datos/procesados/`: Datos limpios (`winequality_cleaned.csv`) listos para modelos predictivos o análisis final.
* `cuadernos/`:
  * `01_EDA_and_Wrangling.ipynb`: Cuaderno principal con el paso a paso detallado desde la ingestión y limpieza de los datos hasta el EDA inicial.
  * `02_Resumen_Analisis.ipynb`: Cuaderno ejecutivo que resume directamente los hallazgos gráficos y conclusiones sobre la calidad, tipo de vino y alcohol.
  * `analysis_results.md`: Reporte estático con las gráficas exportadas y sus conclusiones.
* `codigo/`: Carpeta para futuros scripts modulares en Python.

## 2. Flujo de Trabajo y Metodología

El análisis se desarrolló siguiendo este pipeline estricto:

### A. Exploración Inicial (EDA) y Data Wrangling
* **Unión de Conjuntos**: Se combinaron los datos de vino blanco y tinto en un único *DataFrame*, agregando una columna categórica `wine_type`.
* **Limpieza**: Se identificaron múltiples registros duplicados en la base de datos cruda. Estos fueron eliminados para evitar sesgos, reduciendo el ruido en la muestra.
* **Exportación**: El dataset resultante se guardó en `datos/procesados/winequality_cleaned.csv` para asegurar que todo análisis posterior parta de una fuente de verdad verificada y limpia.

### B. Análisis de Resultados (A partir de datos limpios)
Una vez limpios los datos, procedimos a responder preguntas clave de negocio utilizando herramientas de visualización (`seaborn` y `matplotlib`):

1. **Análisis de la Calidad y Tipo de Vino**:
   Descubrimos que la calidad promedio para ambos tipos de vino es idéntica (puntuación de 6). Sin embargo, el vino blanco presenta una concentración proporcionalmente mayor en las puntuaciones de "alta calidad" (7 y 8).

2. **Diferencias Químicas Clave (Acidez Volátil)**:
   Al analizar las densidades químicas, encontramos una diferencia drástica en la **Acidez Volátil**. El vino blanco mantiene niveles bajísimos y sumamente controlados para conservar su frescura (ya que el exceso produce sabor a vinagre). El vino tinto, por su naturaleza tánica, tolera y presenta niveles significativamente mayores.

3. **Análisis de Alcohol**:
   Se investigó si el alcohol era un factor diferenciador. Estadísticamente, el vino blanco tiene una media levísimamente superior (10.59% frente a 10.43%), pero el tinto posee el valor atípico más extremo (14.9%). A pesar de esto, el 50% central de todos los vinos se encuentra en el mismo rango (9.5% a 11.4%), indicando que la industria estandariza el grado alcohólico para el consumidor final independientemente del tipo de uva.

## 3. Configuración del Entorno Local

1. Crea tu entorno virtual: `python3 -m venv venv`
2. Actívalo: `source venv/bin/activate` (Mac/Linux) o `venv\Scripts\activate` (Windows)
3. Instala dependencias: `pip install -r requirements.txt`
4. Ejecuta los cuadernos: `jupyter notebook`

## Diccionario de Datos de Referencia

| Nombre | Tipo de Variable | Interpretación |
|---|---|---|
| **fixed acidity** | Numérica Continua | Ácidos que no se evaporan fácilmente. |
| **volatile acidity** | Numérica Continua | Ácido acético. Niveles altos dan sabor a vinagre. |
| **citric acid** | Numérica Continua | Añade "frescura" y sabor en pequeñas cantidades. |
| **residual sugar** | Numérica Continua | Azúcar residual. Determina el dulzor. |
| **chlorides** | Numérica Continua | Cantidad de sal en el vino. |
| **free sulfur dioxide** | Numérica Continua | Previene crecimiento microbiano y oxidación. |
| **total sulfur dioxide** | Numérica Continua | Sobre 50 ppm afecta olor y sabor. |
| **density** | Numérica Continua | Densidad del vino en g/cm³. |
| **pH** | Numérica Continua | Escala de acidez (0-14). Mayoría entre 3 y 4. |
| **sulphates** | Numérica Continua | Aditivo antimicrobiano/antioxidante. |
| **alcohol** | Numérica Continua | Porcentaje de alcohol por volumen. |
| **quality** | Numérica Discreta | **Variable Objetivo**. Puntuación sensorial (0 a 10). |
| **wine_type** | Categórica Nominal | Indica si el vino es tinto ('red') o blanco ('white'). |
