# src/producto.py
class Producto:
    def __init__(self, id, nombre, cantidad, precio):
        self.id = id
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    def __str__(self):
        return f"{self.id} | {self.nombre} | {self.cantidad} | ${self.precio:.2f}"

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "cantidad": self.cantidad,
            "precio": self.precio
        }

    @staticmethod
    def from_dict(data):
        return Producto(
            id=data["id"],
            nombre=data["nombre"],
            cantidad=data["cantidad"],
            precio=data["precio"]
        )
