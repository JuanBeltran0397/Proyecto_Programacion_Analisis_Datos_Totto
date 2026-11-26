import json
import os
import pandas as pd


DATA_PATH = "data/totto_ejecutivos.csv"
OUTPUT_HTML = "docs/index.html"


def generar_html(ruta_csv=DATA_PATH, ruta_salida=OUTPUT_HTML):
    """Genera un dashboard HTML interactivo a partir del CSV extraído."""
    if not os.path.exists(ruta_csv):
        raise FileNotFoundError(f"No se encontró el archivo de datos: {ruta_csv}")

    df = pd.read_csv(ruta_csv)
    os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)

    total_productos = len(df)
    precio_promedio = f"${df['precio_cop'].mean():,.0f}" if total_productos > 0 else "$0"
    descuento_promedio = f"{df['descuento_pct'].mean():.1f}%" if total_productos > 0 else "0%"
    disponibles = int(df["disponible"].sum()) if total_productos > 0 else 0
    fecha_act = (
        df["fecha_extraccion"].iloc[0]
        if total_productos > 0 and "fecha_extraccion" in df.columns
        else "Sin fecha"
    )

    # Preparar datos para gráficos (Top 10 precios y Top 10 descuentos)
    top_precios = df.nlargest(10, "precio_cop")[["nombre", "precio_cop"]]
    labels_precios = json.dumps(top_precios["nombre"].tolist(), ensure_ascii=False)
    valores_precios = json.dumps(top_precios["precio_cop"].tolist())

    con_desc = df[df["descuento_pct"] > 0].nlargest(10, "descuento_pct")[
        ["nombre", "descuento_pct"]
    ]
    labels_desc = json.dumps(con_desc["nombre"].tolist(), ensure_ascii=False)
    valores_desc = json.dumps(con_desc["descuento_pct"].tolist())

    # Construir filas de la tabla HTML
    filas_html = []
    for _, row in df.iterrows():
        estado_badge = (
            '<span class="badge ok">Disponible</span>'
            if row["disponible"]
            else '<span class="badge no">Agotado</span>'
        )
        enlace = (
            f'<a href="{row["url"]}" target="_blank" rel="noopener">Ver en Totto</a>'
            if pd.notna(row["url"]) and str(row["url"]).strip()
            else "-"
        )
        filas_html.append(
            f"""
            <tr>
                <td>{row['nombre']}</td>
                <td>{row['categoria']}</td>
                <td>${row['precio_cop']:,.0f}</td>
                <td>${row['precio_lista_cop']:,.0f}</td>
                <td>{row['descuento_pct']:.1f}%</td>
                <td>{estado_badge}</td>
                <td>{enlace}</td>
            </tr>
            """
        )

    tabla_cuerpo = "\n".join(filas_html)

    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reporte Automatizado — Catálogo Totto Colombia</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f4f6f9; color: #222; margin: 0; padding: 24px;
        }}
        .container {{ max-width: 1200px; margin: auto; }}
        header {{
            background: #1a1a1a; color: #fff; padding: 24px;
            border-radius: 10px; margin-bottom: 24px;
        }}
        header h1 {{ margin: 0 0 8px 0; font-size: 1.6rem; }}
        header p {{ margin: 0; color: #ccc; font-size: 0.95rem; }}
        .kpis {{
            display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 16px; margin-bottom: 24px;
        }}
        .card {{
            background: #fff; padding: 20px; border-radius: 10px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.06);
        }}
        .card h3 {{ margin: 0 0 8px 0; font-size: 0.9rem; color: #666; text-transform: uppercase; }}
        .card .valor {{ font-size: 1.8rem; font-weight: bold; color: #d32f2f; }}
        .charts {{
            display: grid; grid-template-columns: repeat(auto-fit, minmax(450px, 1fr));
            gap: 20px; margin-bottom: 24px;
        }}
        .table-box {{
            background: #fff; padding: 20px; border-radius: 10px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.06); overflow-x: auto;
        }}
        #buscador {{
            width: 100%; max-width: 400px; padding: 10px;
            margin-bottom: 16px; border: 1px solid #ccc; border-radius: 6px;
        }}
        table {{ width: 100%; border-collapse: collapse; font-size: 0.92rem; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #eee; }}
        th {{ background: #f8f9fa; font-weight: 600; }}
        tr:hover {{ background: #fafafa; }}
        .badge {{ padding: 4px 8px; border-radius: 12px; font-size: 0.8rem; font-weight: bold; }}
        .badge.ok {{ background: #e8f5e9; color: #2e7d32; }}
        .badge.no {{ background: #ffebee; color: #c62828; }}
        a {{ color: #d32f2f; text-decoration: none; font-weight: 600; }}
    </style>
</head>
<body>
<div class="container">
    <header>
        <h1>🎒 Monitor Automatizado — Morrales Totto Colombia</h1>
        <p>Pipeline CI/CD (GitHub Actions) | Última actualización: <strong>{fecha_act}</strong></p>
    </header>

    <section class="kpis">
        <div class="card">
            <h3>Productos Analizados</h3>
            <div class="valor">{total_productos}</div>
        </div>
        <div class="card">
            <h3>Precio Promedio (COP)</h3>
            <div class="valor">{precio_promedio}</div>
        </div>
        <div class="card">
            <h3>Descuento Promedio</h3>
            <div class="valor">{descuento_promedio}</div>
        </div>
        <div class="card">
            <h3>Disponibles en Stock</h3>
            <div class="valor">{disponibles}</div>
        </div>
    </section>

    <section class="charts">
        <div class="card">
            <h3>Top 10 Productos con Mayor Precio (COP)</h3>
            <canvas id="chartPrecios"></canvas>
        </div>
        <div class="card">
            <h3>Top 10 Mayores Descuentos (%)</h3>
            <canvas id="chartDescuentos"></canvas>
        </div>
    </section>

    <section class="table-box">
        <h3>Catálogo Detallado Extraído</h3>
        <input type="text" id="buscador" onkeyup="filtrarTabla()"
               placeholder="Filtrar producto por nombre...">
        <table id="tablaProductos">
            <thead>
                <tr>
                    <th>Producto</th>
                    <th>Categoría</th>
                    <th>Precio Actual</th>
                    <th>Precio Lista</th>
                    <th>Descuento</th>
                    <th>Estado</th>
                    <th>Enlace</th>
                </tr>
            </thead>
            <tbody>
                {tabla_cuerpo}
            </tbody>
        </table>
    </section>
</div>

<script>
    new Chart(document.getElementById('chartPrecios'), {{
        type: 'bar',
        data: {{
            labels: {labels_precios},
            datasets: [{{
                label: 'Precio COP',
                data: {valores_precios},
                backgroundColor: '#d32f2f'
            }}]
        }},
        options: {{ indexAxis: 'y', plugins: {{ legend: {{ display: false }} }} }}
    }});

    new Chart(document.getElementById('chartDescuentos'), {{
        type: 'bar',
        data: {{
            labels: {labels_desc},
            datasets: [{{
                label: 'Descuento %',
                data: {valores_desc},
                backgroundColor: '#2e7d32'
            }}]
        }},
        options: {{ indexAxis: 'y', plugins: {{ legend: {{ display: false }} }} }}
    }});

    function filtrarTabla() {{
        const filtro = document.getElementById('buscador').value.toLowerCase();
        const filas = document.querySelectorAll('#tablaProductos tbody tr');
        filas.forEach(fila => {{
            const texto = fila.cells[0].textContent.toLowerCase();
            fila.style.display = texto.includes(filtro) ? '' : 'none';
        }});
    }}
</script>
</body>
</html>
"""

    with open(ruta_salida, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Reporte HTML generado exitosamente en: {ruta_salida}")


if __name__ == "__main__":
    generar_html()
