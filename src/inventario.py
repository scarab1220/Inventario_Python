# src/inventario.py
from src.producto import Producto
import uuid

class Inventario:
    def __init__(self):
        self.productos = []

    def agregar(self, nombre, cantidad, precio):
        id = str(uuid.uuid4())[:8]
        producto = Producto(id, nombre, cantidad, precio)
        self.productos.append(producto)

    def listar(self):
        return self.productos

    def buscar(self, id):
        for producto in self.productos:
            if producto.id == id:
                return producto
        return None

    def actualizar(self, id, nombre, cantidad, precio):
        producto = self.buscar(id)
        if producto:
            producto.nombre = nombre
            producto.cantidad = cantidad
            producto.precio = precio
            return True
        return False

    def eliminar(self, id):
        producto = self.buscar(id)
        if producto:
            self.productos.remove(producto)
            return True
        return False
