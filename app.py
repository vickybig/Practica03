from src.procesador import Analizador

def main():
    archivo = "datos/sri_ventas_2024.csv"
    
    analizador = Analizador(archivo)
    print("Ventas totales por provincia:")
    resumen = analizador.ventas_totales_por_provincia()
    for prov, total in resumen.items():
        print(f"\t{prov}: ${total:.2f}")

    print("\nCompras para una provincia")
    provincia = input("\tIngrese el nombre de una provincia: ")
    ventas = analizador.ventas_por_provincia(provincia)
    print(f"\tVentas de {provincia}: ${ventas:,.2f}")

    print("1) Ventas totales por provincia (muestra 10):")
    resumen = analizador.ventas_totales_por_provincia()
    for i, (prov, total) in enumerate(sorted(resumen.items(), key=lambda kv: kv[0])):
        if i >= 10: break
        print(f"\t{prov}: ${total:,.2f}")

    print("\n2) Exportaciones totales por mes:")
    expmes = analizador.exportaciones_totales_por_mes()
    for mes, total in sorted(expmes.items()):
        print(f"\t{mes}: ${total:,.2f}")

    print("\n3) Porcentaje ventas tarifa 0% por provincia (muestra 10):")
    pct = analizador.porcentaje_ventas_tarifa_0_por_provincia()
    for i, (prov, porcentaje) in enumerate(sorted(pct.items(), key=lambda kv: kv[0])):
        if i >= 10: break
        print(f"\t{prov}: {porcentaje:.2f}%")

    print("\n4) Provincia con mayor importaciones:")
    prov_max, monto = analizador.provincia_con_mayor_importaciones()
    print(f"\t{prov_max}: ${monto:,.2f}")

if __name__ == "__main__":
    main()