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

    def agregar(self, nombre, cantidad, precio, categoria):
        nuevo_producto = Producto(nombre, cantidad, precio, categoria)
        self._productos.append(nuevo_producto)
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

    def eliminar_categoria(self, nombre_categoria):
        """
        Elimina la categoría por nombre y elimina la referencia en los productos.
        Retorna True si se eliminó, False si no existe.
        """
        # Elimina la categoría de la lista interna
        categorias_filtradas = [c for c in self._categorias if c.nombre != nombre_categoria]
        if len(categorias_filtradas) == len(self._categorias):
            return False  # No se encontró la categoría
        self._categorias = categorias_filtradas

        for producto in self._productos:
            if getattr(producto, "categoria", None) == nombre_categoria:
                producto.categoria = "Sin categoría" # Asignar una categoría por defecto, por recomendacion del docente
        self.guardar()
        return True

def actualizar_tabla(tabla, inventario):
    tabla.delete(*tabla.get_children())
    for p in inventario.listar():
        tabla.insert(
            "", "end", iid=p.id,
            values=(p.id, p.nombre, p.cantidad, f"${p.precio:.2f}", getattr(p, "categoria", ""))
        )