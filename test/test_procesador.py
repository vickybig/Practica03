import unittest
import sys
import os    # ← ESTE IMPORT ES OBLIGATORIO
import csv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.procesador import Analizador, _parse_float
from collections import defaultdict

CSV_PATH = os.path.join("datos", "sri_ventas_2024.csv")


class TestAnalizador(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.analizador = Analizador(CSV_PATH)

    def test_ventas_totales_como_diccionario(self):
        resumen = self.analizador.ventas_totales_por_provincia()
        self.assertIsInstance(resumen, dict, "ventas_totales_por_provincia debe retornar un dict")

    def test_provincias_consultadas_existen(self):
        with open(CSV_PATH, newline="", encoding="utf-8", errors="replace") as f:
            lector = csv.DictReader(f, delimiter="|")  # ← CORRECCIÓN AQUÍ
            provincias = []
            for r in lector:
                p = (r.get("PROVINCIA") or "").strip()
                if p and p not in provincias:
                    provincias.append(p)
                if len(provincias) >= 3:
                    break

        self.assertTrue(len(provincias) >= 1, "El CSV no contiene provincias válidas para probar")

        for p in provincias:
            v = self.analizador.ventas_por_provincia(p)
            self.assertIsInstance(v, float)
            self.assertGreaterEqual(v, 0.0)

    def test_valores_tres_provincias_correctos(self):
        with open(CSV_PATH, newline="", encoding="utf-8", errors="replace") as f:
            lector = csv.DictReader(f, delimiter="|")  # ← CORRECCIÓN AQUÍ
            acc = defaultdict(float)
            for r in lector:
                p = (r.get("PROVINCIA") or "").strip()
                tv = r.get("TOTAL_VENTAS") or r.get("TOTAL VENTAS") or "0"
                acc[p] += _parse_float(tv)

        resumen = self.analizador.ventas_totales_por_provincia()
        provincias = [p for p in acc.keys() if p][:3]

        self.assertTrue(len(provincias) >= 1)

        for p in provincias:
            esperado = acc[p]
            obtenido = resumen.get(p, 0.0)
            self.assertAlmostEqual(esperado, obtenido, places=2, msg=f"Desacuerdo en provincia {p}")


    def test_porcentaje_tarifa_0_por_provincia(self):
        pct = self.analizador.porcentaje_ventas_tarifa_0_por_provincia()
        self.assertIsInstance(pct, dict)
        # verifica que los porcentajes sean numéricos y no negativos
        for k, v in pct.items():
            self.assertIsInstance(v, (int, float))
            self.assertGreaterEqual(v, 0.0)
            # opcional: aseguramos que no sea NaN
            self.assertFalse(v != v)  # True sólo si NaN



    def test_exportaciones_totales_por_mes(self):
        res = self.analizador.exportaciones_totales_por_mes()
        self.assertIsInstance(res, dict)
        for v in res.values():
            self.assertIsInstance(v, (int, float))
            self.assertGreaterEqual(v, 0.0)

    def test_provincia_con_mayor_importaciones(self):
        prov, monto = self.analizador.provincia_con_mayor_importaciones()
        self.assertIsInstance(prov, str)
        self.assertIsInstance(monto, float)
        self.assertGreaterEqual(monto, 0.0)


if __name__ == "__main__":
    unittest.main()