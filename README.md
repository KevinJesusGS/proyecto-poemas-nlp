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

# Estructura del proyecto

```text
proyecto-poemas-nlp/
│
├── data/
│   ├── poemas.csv
│   └── diccionario_palabras.csv
│
├── results/
│   ├── generados/
│   ├── visualizaciones/
│   ├── vocabulario/
│   ├── embeddings/
│   └── estadisticas/
│
├── src/
│   ├── generacion/
│   ├── analisis/
│   ├── visualizacion/
│   └── bigdata/
│
├── main.py
├── run.py
├── requirements.txt
└── README.md