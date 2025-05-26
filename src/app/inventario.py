from app.producto import Producto
from app.categoria import Categoria
import uuid

class Inventario:
    def __init__(self, storage):
        self._productos = []
        self._categorias = []
        self._storage = storage

    def cargar(self):
        self._productos = self._storage.cargar()

    def guardar(self):
        self._storage.guardar(self._productos)

    def agregar(self, nombre, cantidad, precio):
        id = str(uuid.uuid4())[:8]
        producto = Producto(id, nombre, cantidad, precio)
        self._productos.append(producto)
        self.guardar()

    def listar(self):
        return self._productos

    def buscar(self, id):
        for producto in self._productos:
            if producto.id == id:
                return producto
        return None

    def actualizar(self, id, nombre, cantidad, precio, categoria):
        producto = self.buscar(id)
        if producto:
            producto.nombre = nombre
            producto.cantidad = cantidad
            producto.precio = precio
            producto.categoria = categoria
            self.guardar()
            return True
        return False

    def eliminar(self, id):
        producto = self.buscar(id)
        if producto:
            self._productos.remove(producto)
            self.guardar()
            return True
        return False

    def agregar_producto(self, producto):
        self._productos.append(producto)

    def agregar_categoria(self, nombre):
        if nombre not in [c.nombre for c in self._categorias]:
            self._categorias.append(Categoria(nombre))
            return True
        return False

    def set_categorias(self, categorias):
        self._categorias = categorias

    def listar_categorias(self):
        return self._categorias
    
    def buscar_categoria(self, id):
        for categoria in self._categorias:
            if categoria.id == id:
                return categoria
        return None