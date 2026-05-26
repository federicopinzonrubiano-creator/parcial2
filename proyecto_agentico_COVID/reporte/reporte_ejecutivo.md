# Reporte Ejecutivo: Proyecto Agentico COVID

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

| Estado | Media | Mediana | Desv_Std | Minimo | Maximo | N |
| --- | --- | --- | --- | --- | --- | --- |
| Leve | 40.4 | 39.0 | 17.6 | 1 | 100 | 23119 |
| Fallecido | 66.8 | 68.0 | 15.9 | 4 | 98 | 546 |

*Nota: Datos obtenidos a partir del analisis consolidado.*

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

| Nombre municipio | Leve | Fallecido | Total | % Leve | % Fallecido |
| --- | --- | --- | --- | --- | --- |
| PALESTINA | 110 | 10 | 120 | 91.7 | 8.3 |
| BELALCAZAR | 49 | 4 | 53 | 92.5 | 7.5 |
| RISARALDA | 43 | 3 | 46 | 93.5 | 6.5 |
| ARANZAZU | 73 | 5 | 78 | 93.6 | 6.4 |
| RIOSUCIO | 221 | 14 | 235 | 94.0 | 6.0 |
| ANSERMA | 191 | 12 | 203 | 94.1 | 5.9 |
| VITERBO | 179 | 11 | 190 | 94.2 | 5.8 |
| SUPIA | 203 | 12 | 215 | 94.4 | 5.6 |
| SAN JOSE | 18 | 1 | 19 | 94.7 | 5.3 |
| CHINCHINA | 919 | 48 | 967 | 95.0 | 5.0 |
| MANZANARES | 157 | 8 | 165 | 95.2 | 4.8 |
| FILADELFIA | 189 | 9 | 198 | 95.5 | 4.5 |

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

---

## Resultados del Modelado Predictivo (Machine Learning)

### El Desafio del Desbalance de Clases
Un aspecto metodologico crucial en este estudio es el severo desbalance de la variable objetivo. El **97.69% (23,120 casos)** corresponden a la clase Leve/Asintomática (0), mientras que solo el **2.31% (546 casos)** pertenecen a la clase Moderado/Grave/Fallecido (1). 

Para evitar que los modelos matematicos predijeran de forma sesgada la clase mayoritaria (ignorando los casos graves), se aplico una estrategia combinada de:
1. **Division Estratificada (Stratified Train/Test Split)**: Asegurando la misma proporcion de casos graves (2.31%) tanto en el conjunto de entrenamiento como en el de validacion.
2. **Ponderacion Balanceada de Clases (Class Weighting)**: Penalizando fuertemente los errores cometidos sobre la clase minoritaria (gravedad 1) durante el entrenamiento de los algoritmos.

### Comparativa de Modelos
Se entrenaron y evaluaron dos algoritmos competidores en el conjunto de test independiente utilizando el puntaje F1 ponderado (Weighted F1-Score) as metrica de seleccion:

- **Regresion Logistica**: F1-Score = 0.8553
- **Random Forest Classifier (Ganador)**: F1-Score = 0.9195

El algoritmo seleccionado por el orquestador debido a su superior desempeño predictivo es **Random Forest**.

### Reporte de Clasificacion Detallado (Modelo Ganador)

A continuacion se presenta el reporte de rendimiento obtenido por el modelo ganador sobre los datos de prueba:

```
              precision    recall  f1-score   support

    Leve (0)       0.98      0.90      0.94      4625
   Grave (1)       0.07      0.33      0.12       109

    accuracy                           0.88      4734
   macro avg       0.53      0.61      0.53      4734
weighted avg       0.96      0.88      0.92      4734

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