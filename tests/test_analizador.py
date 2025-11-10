import unit





















import pytest
from procesador import Analizador

# Creamos un CSV de ejemplo para las pruebas
import csv
import os

@pytest.fixture(scope="module")
def archivo_prueba(tmp_path):
    """Crea un archivo CSV temporal con datos de prueba."""
    ruta = tmp_path / "ventas_test.csv"
    datos = [
        {"PROVINCIA": "Buenos Aires", "TOTAL_VENTAS": "150000"},
        {"PROVINCIA": "Córdoba", "TOTAL_VENTAS": "95000"},
        {"PROVINCIA": "Santa Fe", "TOTAL_VENTAS": "120000"},
        {"PROVINCIA": "Buenos Aires", "TOTAL_VENTAS": "50000"},
    ]

    with open(ruta, mode="w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=["PROVINCIA", "TOTAL_VENTAS"])
        escritor.writeheader()
        escritor.writerows(datos)
    return ruta


@pytest.fixture
def analizador(archivo_prueba):
    """Instancia el analizador con el CSV de prueba."""
    return Analizador(archivo_prueba)


def test_numero_de_provincias(analizador):
    """1. Validar que el número de provincias sea coherente."""
    resultado = analizador.ventas_totales_por_provincia()
    assert len(resultado) == 3, "Debe haber 3 provincias únicas"


def test_valores_numericos_y_no_negativos(analizador):
    """2. Verificar que los valores sean numéricos y no negativos."""
    resultado = analizador.ventas_totales_por_provincia()
    for total in resultado.values():
        assert isinstance(total, (int, float)), "El valor debe ser numérico"
        assert total >= 0, "El valor no puede ser negativo"


def test_retorna_diccionario(analizador):
    """3. Garantizar que la función retorne un diccionario."""
    resultado = analizador.ventas_totales_por_provincia()
    assert isinstance(resultado, dict), "La función debe retornar un diccionario"


def test_provincia_existente(analizador):
    """4. Verificar que las provincias consultadas existan."""
    provincias = ["Buenos Aires", "Córdoba", "Santa Fe"]
    for prov in provincias:
        total = analizador.ventas_por_provincia(prov)
        assert total > 0, f"La provincia {prov} debería existir y tener ventas mayores a 0"


def test_valores_correctos_por_provincia(analizador):
    """5. Verificar que los valores consultados de 3 provincias sean correctos."""
    assert analizador.ventas_por_provincia("Buenos Aires") == 200000.0
    assert analizador.ventas_por_provincia("Córdoba") == 95000.0
    assert analizador.ventas_por_provincia("Santa Fe") == 120000.0
