import os
import pandas as pd
from scraper import (
    obtener_productos_ejecutivos,
    procesar_catalogo,
    ejecutar_pipeline_extraccion,
)


def test_conexion_api_totto():
    """Verifica que la API pública de Totto responda con una lista de productos."""
    datos = obtener_productos_ejecutivos(limite=15)
    assert isinstance(datos, list)
    assert len(datos) > 0


def test_transformacion_y_reglas_negocio():
    """Valida columnas esperadas, precios positivos y cálculo de descuentos."""
    datos = obtener_productos_ejecutivos(limite=30)
    df = procesar_catalogo(datos, solo_ejecutivos=False)

    columnas_requeridas = [
        "product_id",
        "nombre",
        "precio_cop",
        "precio_lista_cop",
        "descuento_pct",
        "disponible",
        "fecha_extraccion",
    ]
    for col in columnas_requeridas:
        assert col in df.columns

    assert len(df) > 0
    assert (df["precio_cop"] > 0).all()
    assert (df["descuento_pct"] >= 0).all()
    assert df["nombre"].isna().sum() == 0


def test_generacion_csv_salida(tmp_path):
    """Comprueba que el pipeline guarde el CSV correctamente en disco."""
    archivo_temporal = tmp_path / "test_totto.csv"
    df_resultado = ejecutar_pipeline_extraccion(str(archivo_temporal))

    assert os.path.exists(archivo_temporal)
    df_leido = pd.read_csv(archivo_temporal)
    assert len(df_leido) == len(df_resultado)
