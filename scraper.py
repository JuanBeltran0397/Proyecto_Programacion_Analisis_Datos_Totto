import os
from datetime import datetime
from zoneinfo import ZoneInfo
import requests
import pandas as pd


BASE_URL = os.getenv("TOTTO_BASE_URL", "https://co.totto.com")
SEARCH_ENDPOINT = f"{BASE_URL}/api/catalog_system/pub/products/search"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
}


def obtener_productos_ejecutivos(limite=1000):
    """Recorre paginadamente el catálogo público de Totto Colombia en lotes de 50."""
    todos_productos = []
    paso = 50

    for inicio in range(0, limite, paso):
        fin = min(inicio + paso - 1, limite - 1)
        params = {"_from": inicio, "_to": fin}
        respuesta = requests.get(
            SEARCH_ENDPOINT, params=params, headers=HEADERS, timeout=20
        )
        # VTEX devuelve 200 (completo) o 206 (parcial paginado); ambos son válidos
        if respuesta.status_code not in (200, 206):
            respuesta.raise_for_status()

        lote = respuesta.json()
        if not lote:
            break

        todos_productos.extend(lote)
        if len(lote) < paso:
            break

    return todos_productos


def procesar_catalogo(productos_raw, solo_ejecutivos=True):
    """Transforma la respuesta JSON cruda en un DataFrame estructurado."""
    registros = []
    zona_colombia = ZoneInfo("America/Bogota")
    fecha_extraccion = datetime.now(zona_colombia).strftime("%Y-%m-%d %H:%M:%S COT")

    for prod in productos_raw:
        product_id = prod.get("productId")
        nombre = prod.get("productName", "").strip()
        descripcion = prod.get("description", "").lower()
        marca = prod.get("brand", "TOTTO")
        categorias = prod.get("categories", [])
        ruta_categorias = " ".join(categorias).lower()

        if solo_ejecutivos and (
            "ejecutivo" not in nombre.lower()
            and "ejecutivo" not in ruta_categorias
            and "ejecutivo" not in descripcion
        ):
            continue

        categoria_principal = categorias[0].strip("/") if categorias else "Morrales"
        url_producto = prod.get("link", "")

        items = prod.get("items", [])
        if not items:
            continue

        sellers = items[0].get("sellers", [])
        if not sellers:
            continue

        oferta = sellers[0].get("commertialOffer", {})
        precio_actual = float(oferta.get("Price", 0))
        precio_lista = float(oferta.get("ListPrice", 0))
        disponible = bool(oferta.get("IsAvailable", False))

        if precio_actual <= 0:
            continue

        descuento_pct = 0.0
        if precio_lista > precio_actual:
            descuento_pct = round(((precio_lista - precio_actual) / precio_lista) * 100, 2)

        registros.append({
            "product_id": str(product_id),
            "nombre": nombre,
            "marca": marca,
            "categoria": categoria_principal,
            "precio_cop": precio_actual,
            "precio_lista_cop": precio_lista,
            "descuento_pct": descuento_pct,
            "disponible": disponible,
            "url": url_producto,
            "fecha_extraccion": fecha_extraccion,
        })

    df = pd.DataFrame(registros)
    if not df.empty:
        df = df.drop_duplicates(subset=["product_id"]).reset_index(drop=True)
    return df


def ejecutar_pipeline_extraccion(ruta_salida="data/totto_ejecutivos.csv"):
    """Ejecuta extracción completa y guarda el archivo CSV."""
    os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)
    datos_crudos = obtener_productos_ejecutivos(limite=1000)
    df_limpio = procesar_catalogo(datos_crudos, solo_ejecutivos=True)

    if df_limpio.empty:
        df_limpio = procesar_catalogo(datos_crudos, solo_ejecutivos=False)

    df_limpio.to_csv(ruta_salida, index=False, encoding="utf-8")
    print(f"Extracción exitosa: {len(df_limpio)} productos guardados en {ruta_salida}")
    return df_limpio


if __name__ == "__main__":
    ejecutar_pipeline_extraccion()
