# Proyecto_Programacion_Analisis_Datos_Totto


## Mejoras implementadas - EA3

### Objetivo

Complementar el sistema automatizado de extracción,
procesamiento, análisis y visualización de datos del
catálogo de morrales ejecutivos de Totto Colombia.

### Mejoras funcionales

- Ampliación de 4 a 8 indicadores.
- Ampliación de 2 a 4 gráficas.
- Análisis del ahorro económico por producto.
- Distribución de productos por categoría.
- Comparación de precios promedio por categoría.
- Filtros por nombre, categoría y rango de precios.
- Contador de productos encontrados.
- Opción para limpiar los filtros.

### Mejoras de calidad

- Ampliación de 3 a 12 pruebas automatizadas.
- Validación de precios y descuentos.
- Validación de indicadores y generación del HTML.
- Análisis estático mediante Flake8.

### Pipeline CI/CD

- Integración continua en la rama mejoras-ea3.
- Ejecución automatizada de pruebas con Pytest.
- Validación de calidad mediante Flake8.
- Extracción automatizada de datos.
- Generación del reporte HTML.
- Restricción del despliegue a la rama main.

### Tecnologías utilizadas

- Python
- Pandas
- Requests
- Pytest
- Flake8
- HTML, CSS y JavaScript
- Chart.js
- GitHub Actions
- GitHub Pages
- Google Colab

### Instalación de dependencias

    pip install -r requirements.txt

### Ejecución del proyecto

    python scraper.py
    python generar_reporte.py

### Ejecución de pruebas

    python -m pytest test_scraper.py test_reporte.py -v

### Resultados de validación local

- 12 pruebas automatizadas aprobadas.
- 8 indicadores en el dashboard.
- 4 gráficas de análisis.

### Control de versiones

Las mejoras se desarrollaron en la rama mejoras-ea3,
conservando el trabajo original del proyecto.
