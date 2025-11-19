"""
🧪 Práctica 03 – Calidad de Software
===================================

Evaluación y pruebas sobre datos del SRI utilizando Python.

Este proyecto implementa un sistema para analizar información contenida en un
archivo CSV del SRI, incluyendo ventas, exportaciones e importaciones. Las
capacidades del sistema abarcan:

- Carga robusta del archivo de datos.
- Obtención de estadísticas por provincia.
- Consultas interactivas desde la terminal.
- Pruebas unitarias desarrolladas con `unittest`.
- Evaluación de cobertura mediante la herramienta `coverage`.

-------------------------------------------------------------

📂 Estructura del proyecto
--------------------------

Practica03-calidad/
│
├── app.py
├── README.md
├── datos/
│   └── sri_ventas_2024.csv
│
├── src/
│   └── procesador.py
│
└── test/
    └── test_procesador.py

-------------------------------------------------------------

🧩 Funcionalidades principales
------------------------------

🔸 1. Cálculo de ventas totales por provincia
    Suma el valor de la columna TOTAL_VENTAS agrupado por provincia.

🔸 2. Consulta de ventas de una provincia específica
    Permite ingresar el nombre de una provincia y muestra su total de ventas.

🔸 3. Exportaciones totales por mes
    Utiliza los campos EXPORTACIONES y MES/PERIODO para generar las estadísticas.

🔸 4. Porcentaje de ventas con tarifa 0%
    Fórmula empleada:
        (VENTAS_NETAS_TARIFA_0 / TOTAL_VENTAS) * 100

🔸 5. Provincia con mayor nivel de importaciones
    Identifica la provincia cuyo valor en la columna IMPORTACIONES es el más alto.

-------------------------------------------------------------

▶️ Ejecución del proyecto
-------------------------

Desde la raíz del proyecto, ejecuta:

    python app.py

-------------------------------------------------------------

"""
