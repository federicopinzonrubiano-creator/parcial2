# Proyecto Agentico COVID

Bienvenido a la documentacion oficial del proyecto predictivo de casos COVID-19. Este proyecto implementa una arquitectura modular basada en **Agentes Analiticos** para garantizar que el codigo sea limpio, escalable y mantenible.

---

## Arquitectura del Proyecto

El sistema esta orquestado por un **Controlador Central** que delega tareas especificas a diferentes modulos denominados "Skills". Esta separacion de responsabilidades aporta grandes beneficios:
1. **Facilita la depuracion:** Si una grafica falla, se revisa la *Skill 2* sin afectar el modelo matematico.
2. **Promueve la escalabilidad:** Facilita la adicion de futuras *Skills* (ej. reportes automaticos).
3. **Flujo secuencial automatizado:** El orquestador garantiza el orden correcto (Limpiar -> Explorar -> Modelar).

### Estructura de Directorios
```text
proyecto_agentico_COVID/

├── orquestador/
│   └── main_orquestador.py         # Cerebro central que coordina el flujo
├── skills/
│   ├── skill_1_wrangling.py        # Limpieza y preparacion de datos
│   ├── skill_2_eda.py              # Analisis exploratorio e imagenes
│   └── skill_3_modelado.py         # Entrenamiento algoritmico y prediccion
├── datos_crudos/                   # Aqui va la Base de datos original (.csv)
├── datos_procesados/               # Aqui se guarda automaticamente el dataset limpio
├── graficos/                       # Carpeta auto-generada con las graficas
└── Guia_Interactiva_Proyecto.ipynb # Notebook de estudio para la defensa
```

---

## Como Ejecutar el Proyecto

1. Asegurate de tener activado tu entorno virtual de Python.
2. Verifica que las librerias base esten instaladas: `pandas`, `scikit-learn`, `matplotlib`, `seaborn`.
3. Ejecuta el archivo principal desde la raiz del proyecto:
   ```bash
   python orquestador/main_orquestador.py
   ```
4. El programa imprimira el paso a paso en consola, guardara un dataset limpio en `datos_procesados/` y generara las imagenes en la carpeta `graficos/`.

---

## Guia de Defensa Oral (Justificacion de Decisiones)

Esta seccion resume metodologicamente el **por que** de las decisiones tomadas en el codigo. Es tu libreto principal para sustentar el trabajo.

### Skill 1: Data Wrangling (Limpieza)
* **Curacion de Columnas:** El dataset original tenia problemas de codificacion (`—` en lugar de acentos). Se soluciono creando un diccionario de mapeo, lo cual demuestra buenas practicas en ingenieria de datos.
* **Feature Selection (Seleccion de Caracteristicas):** Se eliminaron identificadores (`ID de caso`) y fechas descriptivas porque los algoritmos aprenden de caracteristicas inherentes del individuo (Edad, Sexo, Municipio), no de su numero de folio.
* **Feature Engineering (Ingenieria del Target):** Se unifico la variable `Estado` en una nueva variable binaria llamada `Target_Gravedad` (0 = Leve, 1 = Grave/Fallecido). Esto transforma un problema ambiguo en uno de clasificacion clinica clara, facilitando enormemente la prediccion.

### Skill 2: Exploratory Data Analysis (EDA)
* **Evidencia Tangible (Imagenes No-Bloqueantes):** El codigo crea automaticamente la carpeta `evidencias_eda/` y guarda alli los graficos. Esto permite ejecutar el pipeline en servidores sin interfaz grafica de manera desatendida.
* **Tablas de Frecuencia Rigurosas:** Se combinaron las frecuencias absolutas y relativas del Target. Argumenta que esto te permitio descubrir rapidamente si el dataset sufria de un desbalance severo (mayoria de casos leves).
* **Boxplots y Cuartiles:** El grafico de caja es la representacion estadistica optima para ver como se distribuye la gravedad segun la `Edad`, evitando suposiciones visuales ambiguas.
* **Matriz de Correlacion:** Es el puente estadistico hacia la Skill 3. Justifica que el mapa de calor demuestra matematicamente que variables influyen de forma lineal en la gravedad antes de siquiera entrenar un modelo.

### Skill 3: Modelado Predictivo
* **La particion `stratify=y`:** Al dividir los datos en Entrenamiento (80%) y Prueba (20%), la estratificacion garantiza que ambos examenes tengan exactamente la misma proporcion de casos graves y leves, haciendo que la evaluacion del modelo sea matematicamente justa.
* **El parametro `class_weight='balanced'`:** Esta decision arquitectonica es vital en salud. Al haber muchos casos leves, un algoritmo por defecto predecira siempre "Leve" para ganar precision facil. Al balancear los pesos, se obliga al modelo a penalizar duramente cuando se equivoca en diagnosticar un caso verdaderamente grave.
* **Metrica F1-Score vs Exactitud (Accuracy):** La exactitud es enganosa. Si el 90% es leve, decir "Leve" siempre acierta el 90%, pero mata a los graves. Argumenta que usaste el F1-Score ponderado porque este cruza la precision con la sensibilidad, convirtiendolo en el juez mas riguroso para la seleccion automatizada del mejor algoritmo (Regresion Logistica vs Random Forest).
