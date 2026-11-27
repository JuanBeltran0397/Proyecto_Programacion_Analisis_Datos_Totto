
import pandas as pd
import pytest
from generar_reporte import generar_html


# Prueba 1: verificar la generación del dashboard HTML
def test_generacion_dashboard(tmp_path):
    salida = tmp_path / "index.html"

    generar_html(
        "data/totto_ejecutivos.csv",
        str(salida)
    )

    assert salida.exists()
    assert salida.stat().st_size > 0


# Prueba 2: verificar el contenido del dashboard
def test_contenido_dashboard(tmp_path):
    salida = tmp_path / "index.html"

    generar_html(
        "data/totto_ejecutivos.csv",
        str(salida)
    )

    contenido = salida.read_text(encoding="utf-8")

    assert "Totto" in contenido
    assert "<html" in contenido
    assert "<table" in contenido


# Prueba 3: verificar el manejo de archivos inexistentes
def test_archivo_inexistente(tmp_path):
    with pytest.raises(FileNotFoundError):
        generar_html(
            str(tmp_path / "inexistente.csv"),
            str(tmp_path / "index.html")
        )


# Prueba 4: verificar que los precios sean válidos
def test_validacion_precios():
    df = pd.read_csv("data/totto_ejecutivos.csv")

    assert not df.empty
    assert (df["precio_cop"] > 0).all()
    assert (df["precio_lista_cop"] > 0).all()
    assert (df["precio_cop"] <= df["precio_lista_cop"]).all()


# Prueba 5: verificar los porcentajes de descuento
def test_validacion_descuentos():
    df = pd.read_csv("data/totto_ejecutivos.csv")

    assert not df.empty
    assert df["descuento_pct"].between(0, 100).all()


# Prueba 6: verificar el cálculo del ahorro
def test_calculo_ahorro():
    df = pd.read_csv("data/totto_ejecutivos.csv")
    ahorro = df["precio_lista_cop"] - df["precio_cop"]

    assert not df.empty
    assert (ahorro >= 0).all()


# Prueba 7: verificar los indicadores de precios
def test_indicadores_precios():
    df = pd.read_csv("data/totto_ejecutivos.csv")
    precios = df["precio_cop"]

    assert not df.empty
    assert precios.min() <= precios.mean() <= precios.max()


# Prueba 8: verificar la agrupación por categorías
def test_agrupacion_categorias():
    df = pd.read_csv("data/totto_ejecutivos.csv")
    resumen = df.groupby("categoria").size()

    assert not df.empty
    assert resumen.sum() == len(df)


# Prueba 9: verificar los nuevos indicadores del HTML
def test_indicadores_dashboard_ea3(tmp_path):
    salida = tmp_path / "index.html"

    generar_html(
        "data/totto_ejecutivos.csv",
        str(salida)
    )

    contenido = salida.read_text(encoding="utf-8").lower()

    assert "precio mínimo" in contenido
    assert "precio máximo" in contenido
    assert "ahorro promedio" in contenido
    assert "ahorro total" in contenido
