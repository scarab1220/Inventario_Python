import uuid

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

