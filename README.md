# Proyecto_Programacion_Analisis_Datos_Totto

Sistema automatizado de extracción (*web scraping*), procesamiento, análisis y visualización de datos del catálogo de morrales de **Totto Colombia**, con integración y despliegue continuo mediante **GitHub Actions** y **GitHub Pages**.

🌐 **Dashboard en vivo:** [Ver reporte interactivo en GitHub Pages](https://juanbeltran0397.github.io/Proyecto_Programacion_Analisis_Datos_Totto/)

---

## Objetivo del Proyecto

Automatizar la recolección periódica de precios, descuentos y disponibilidad del catálogo de morrales ejecutivos de Totto Colombia para generar un tablero interactivo de indicadores clave (KPIs) y análisis comparativo, garantizando calidad de código y despliegue continuo sin intervención manual.

---

## Mejoras Implementadas — Entrega EA3

### Mejoras funcionales en el Dashboard (`generar_reporte.py`)
- **Ampliación de 4 a 8 indicadores KPI:** incorporación de precio mínimo, precio máximo, ahorro promedio por producto y ahorro total potencial en pesos colombianos (COP).
- **Ampliación de 2 a 4 gráficas interactivas (Chart.js):** Top 10 productos con mayor precio, Top 10 mayores descuentos (%), distribución de productos por categoría y precio promedio por categoría.
- **Análisis económico:** cálculo automático del ahorro por producto (`precio_lista_cop - precio_cop`).
- **Filtros dinámicos en el catálogo:** búsqueda en tiempo real por nombre, filtro por categoría, rango de precios (mínimo y máximo), contador dinámico de resultados y botón para limpiar filtros.
- **Localización horaria:** conversión automática de la marca de tiempo de extracción desde `UTC` a **hora local de Colombia (`COT`, UTC-5)** en formato legible.

### Mejoras de calidad y pruebas (`test_reporte.py`)
- **Ampliación de 3 a 12 pruebas unitarias automatizadas** con `pytest`.
- Validación de cálculos de precios, porcentajes de descuento, ahorro económico y disponibilidad.
- Validación de integridad de indicadores y generación correcta del archivo HTML.
- Análisis estático de estilo y sintaxis bajo estándares PEP 8 mediante **Flake8**.

### Pipeline CI/CD (`.github/workflows/ci_cd.yml`)
- Validación automatizada en ramas de desarrollo (`mejoras-ea3`) y producción (`main`).
- Ejecución automática de pruebas unitarias (`pytest`) y auditoría de código (`flake8`).
- Extracción automatizada del catálogo (`scraper.py`) y regeneración del reporte (`generar_reporte.py`).
- Despliegue continuo automático publicado desde la carpeta `/docs` en la rama `main` hacia **GitHub Pages**.

---

## Estructura del Repositorio

```text
├── .github/workflows/   # Configuración del pipeline CI/CD en GitHub Actions
├── data/                # Dataset extraído en formato CSV (totto_ejecutivos.csv)
├── docs/                # Reporte HTML generado y publicado en GitHub Pages (index.html)
├── scraper.py           # Módulo de extracción de datos desde Totto Colombia
├── generar_reporte.py   # Generador del dashboard HTML interactivo con Chart.js
├── test_scraper.py      # Pruebas unitarias del módulo de extracción
├── test_reporte.py      # Pruebas unitarias del generador de reportes y métricas
├── requirements.txt     # Dependencias del proyecto
└── README.md            # Documentación técnica del proyecto
