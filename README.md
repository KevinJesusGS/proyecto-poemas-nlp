# Generador Inteligente de Poemas en Español 

Sistema de generación automática de poemas en español utilizando técnicas de Procesamiento de Lenguaje Natural (NLP), análisis léxico y generación basada en rimas, vocabulario contextual y refuerzo semántico.

---

# Descripción

Este proyecto implementa un generador de poesía capaz de construir poemas originales en español utilizando:

- Rimas automáticas
- Refuerzo léxico
- Vocabulario contextual
- Análisis de terminaciones
- Integración de diccionarios externos
- Generación temática
- Métricas lingüísticas
- Persistencia automática de resultados

El sistema combina versos reales y versos sintéticos para producir poemas coherentes con estructuras poéticas configurables.

---

# Características

##  Generación automática de poemas

- Generación por temas
- Construcción automática de versos
- Poemas multi-párrafo
- Control de longitud
- Patrones de rima configurables

---

## Sistema de rimas inteligente

- Detección automática de rimas
- Rima flexible
- Comparación fonética parcial
- Agrupación por terminaciones

---

## Refuerzo de vocabulario

- Diccionarios externos
- Expansión léxica
- Integración temática
- Selección contextual de palabras

---

## NLP y análisis textual

- Limpieza de texto
- Tokenización
- Diversidad léxica
- Estadísticas lingüísticas
- Embeddings TF-IDF

---

## Exportación automática

El sistema guarda automáticamente:

- Poemas generados
- Métricas
- Archivos JSON
- Estadísticas
- Visualizaciones

---

# Ejecución

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Ejecutar proyecto principal:

```bash
python run.py
```

Ejecutar análisis Big Data:

```bash
python ejemplo_bigdata.py
```

Ejecutar integración con HuggingFace:

```bash
python ejemplo_huggingface_bigdata.py
```

# Estructura del proyecto

```bash
proyecto-poemas-nlp/
│
├── data/                          # Datasets y diccionarios
│
├── results/                       # Resultados generados
│
├── src/
│   │
│   ├── analysis/                  # Análisis de estilo y vocabulario
│   │   ├── analizar_estilo.py
│   │   └── analizar_vocabulario.py
│   │
│   ├── bigdata/                   # Procesamiento Big Data con PySpark
│   │   ├── analisis_huggingface.py
│   │   ├── cargar_dataset_hf.py
│   │   ├── spark_estadisticas.py
│   │   ├── spark_preprocesamiento.py
│   │   ├── spark_session.py
│   │   ├── spark_similitud.py
│   │   └── spark_vocabulario.py
│   │
│   ├── generation/                # Generación de poemas
│   │   ├── generar_poemas.py
│   │   ├── generar_poemas_por_topico.py
│   │   └── generar_poemas_refuerzo.py
│   │
│   ├── procesamiento/             # Limpieza y procesamiento de texto
│   │
│   ├── utils/                     # Funciones auxiliares
│   │   └── leer_csv.py
│   │
│   ├── visualization/             # Visualización y resultados
│   │   └── resultados.py
│   │
│   ├── __init__.py
│   └── main.py
│
├── ejemplo_bigdata.py             # Ejemplo de uso con PySpark
├── ejemplo_huggingface_bigdata.py # Ejemplo con HuggingFace
├── run.py                         # Ejecución principal del proyecto
├── requirements.txt
├── .gitignore
└── README.md
```