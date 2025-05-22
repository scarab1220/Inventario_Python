# src/storage.py
import json
from producto import Producto

def cargar_datos(ruta):
    productos = []
    try:
        with open(ruta, "r") as f:
            datos = json.load(f)
            for item in datos:
                productos.append(Producto.from_dict(item))
    except FileNotFoundError:
        pass
    return productos

def guardar_datos(ruta, productos):
    with open(ruta, "w") as f:
        json.dump([p.to_dict() for p in productos], f, indent=4)
