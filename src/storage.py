def load_data(ruta):
    inventario = []
    try:
        with open(ruta, "r") as f:
            for linea in f:
                partes = linea.strip().split("|")
                if len(partes) == 4:
                    inventario.append({
                        "id": partes[0],
                        "nombre": partes[1],
                        "cantidad": int(partes[2]),
                        "precio": float(partes[3])
                    })
    except FileNotFoundError:
        pass
    return inventario

def guardar_datos(ruta, inventario):
    with open(ruta, "w") as f:
        for p in inventario:
            linea = f"{p['id']}|{p['nombre']}|{p['cantidad']}|{p['precio']}\n"
            f.write(linea)