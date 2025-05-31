import uuid
import csv
from tkinter import messagebox

class Producto:
    def __init__(self, nombre, cantidad, precio, categoria, id=None):
        self.id = id or str(uuid.uuid4())
        self.nombre = nombre
        self.cantidad = int(cantidad)
        self.precio = float(precio)
        self.categoria = categoria

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "cantidad": self.cantidad,
            "precio": self.precio,
            "categoria": self.categoria
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            nombre=data["nombre"],
            cantidad=int(data["cantidad"]),
            precio=float(data["precio"]),
            categoria=data.get("categoria", ""),
            id=data.get("id")
        )
    
    @classmethod
    def importar_desde_csv(cls, nombre_archivo="productos.csv"):
        productos = []
        try:
            with open(nombre_archivo, mode='r', newline='', encoding='utf-8') as archivo_csv:
                lector = csv.DictReader(archivo_csv)
                for fila in lector:
                    producto = cls(
                        id=fila['ID'],
                        nombre=fila['Nombre'],
                        cantidad=int(fila['Cantidad']),
                        precio=float(fila['Precio']),
                        categoria=fila.get('Categoria', "")
                    )
                    productos.append(producto)
            return productos
        except FileNotFoundError:
            messagebox.showerror("Error", f"El archivo {nombre_archivo} no se encontró.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo importar los productos: {e}")
            return []