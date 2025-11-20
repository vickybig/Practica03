import csv
from collections import defaultdict
from typing import Dict, Tuple

def _parse_float(value) -> float:
    """Convierte distintos formatos a float de forma robusta."""
    if value is None:
        return 0.0
    if isinstance(value, (int, float)):
        return float(value)
    s = str(value).strip()
    if s == "":
        return 0.0
    s = s.replace("$", "").replace(" ", "")
    s = s.replace(",", "")  # elimina separadores de miles
    if s.startswith("(") and s.endswith(")"):
        s = "-" + s[1:-1]
    try:
        return float(s)
    except Exception:
        cleaned = "".join(ch for ch in s if ch.isdigit() or ch in ".-")
        if cleaned == "":
            return 0.0
        try:
            return float(cleaned)
        except Exception:
            return 0.0

class Analizador:
    def __init__(self, ruta_csv: str, encoding: str = "utf-8"):
        self.ruta_csv = ruta_csv
        self.encoding = encoding
        self.datos = self.leer_csv()

    def leer_csv(self):
        """
        Lee el CSV en modo tolerante con detección simple del delimitador.
        Normaliza los encabezados a MAYÚSCULAS.
        """
        posibles = [",", "|", ";", "\t"]
        sample = ""
        with open(self.ruta_csv, "r", encoding=self.encoding, errors="replace") as f:
            sample = f.read(2048)
        delim = None
        for d in posibles:
            if d in sample:
                delim = d
                break
        if delim is None:
            delim = ","

        datos = []
        with open(self.ruta_csv, "r", encoding=self.encoding, errors="replace") as f:
            lector = csv.DictReader(f, delimiter="|")
            for fila in lector:
                # normalizar keys
                fila_norm = {}
                for k, v in fila.items():
                    if k is None:
                        continue
                    key = k.strip().upper()
                    fila_norm[key] = v
                datos.append(fila_norm)
        return datos

    def ventas_totales_por_provincia(self):
        """
        Suma TOTAL_VENTAS agrupadas por PROVINCIA usando los datos cargados.
        Usa self.datos para asegurar encabezados en mayúsculas.
        """
        acc = defaultdict(float)

        for fila in self.datos:
            prov = fila.get("PROVINCIA", "").strip()
            total = _parse_float(fila.get("TOTAL_VENTAS", 0))
            acc[prov] += total

        return dict(acc)



    def ventas_por_provincia(self, nombre: str) -> float:
        """
        Retorna el total de una provincia
        """
        if not nombre:
            return 0.0
        nombre_busc = nombre.strip().lower()
        resumen = self.ventas_totales_por_provincia()
        for prov, val in resumen.items():
            if prov.strip().lower() == nombre_busc:
                return float(val)
        return 0.0

    #Trabajo autonomo: estadísticas

    def exportaciones_totales_por_mes(self) -> Dict[str, float]:
        """
        Suma EXPORTACIONES agrupadas por MES 
        Retorna dict {mes: total_exportaciones}.
        """
        acc = defaultdict(float)
        for fila in self.datos:
            mes = (fila.get("MES") or fila.get("PERIODO") or "").strip()
            exp = _parse_float(fila.get("EXPORTACIONES") or 0)
            acc[mes] += exp
        return dict(acc)

    def porcentaje_ventas_tarifa_0_por_provincia(self) -> Dict[str, float]:
        """
        Calcula por provincia el porcentaje (VENTAS_NETAS_TARIFA_0 / TOTAL_VENTAS) * 100.
        Retorna dict {provincia: porcentaje}. Si TOTAL_VENTAS == 0 -> porcentaje 0.0.
        """
        numeradores = defaultdict(float)
        denominadores = defaultdict(float)

        for fila in self.datos:
            prov = (fila.get("PROVINCIA") or "").strip()
            v0 = _parse_float(fila.get("VENTAS_NETAS_TARIFA_0") or fila.get("VENTAS NETAS TARIFA 0") or 0)
            tv = _parse_float(fila.get("TOTAL_VENTAS") or fila.get("TOTAL VENTAS") or 0)

            numeradores[prov] += v0
            denominadores[prov] += tv

        resultados = {}
        for prov in set(list(numeradores.keys()) + list(denominadores.keys())):
            denom = denominadores.get(prov, 0.0)
            if denom <= 0.0:
                resultados[prov] = 0.0
            else:
                resultados[prov] = (numeradores.get(prov, 0.0) / denom) * 100.0

        return resultados




    def provincia_con_mayor_importaciones(self) -> Tuple[str, float]:
        """
        Identifica la provincia con mayor total de IMPORTACIONES.
        Retorna (provincia, total) o ("", 0.0) si no hay datos.
        """
        acc = defaultdict(float)
        for fila in self.datos:
            prov = (fila.get("PROVINCIA") or "").strip()
            imp = _parse_float(fila.get("IMPORTACIONES") or 0)
            acc[prov] += imp
        if not acc:
            return ("", 0.0)
        prov_max, monto = max(acc.items(), key=lambda kv: kv[1])
        return prov_max, monto