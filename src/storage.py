# src/storage.py
import json
from producto import Producto

class JsonStorage:
    def __init__(self, ruta):
        self.ruta = ruta

    def cargar(self):
        productos = []
        try:
            with open(self.ruta, "r") as f:
                datos = json.load(f)
                for item in datos:
                    productos.append(Producto.from_dict(item))
        except FileNotFoundError:
            pass
        return productos

    def guardar(self, productos):
        with open(self.ruta, "w") as f:
            json.dump([p.to_dict() for p in productos], f, indent=4)
