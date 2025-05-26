class Producto:
    def __init__(self, id, nombre, cantidad, precio, categoria=None):
        self.id = id
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio
        self.categoria = categoria

    def __str__(self):
        return f"{self.id} | {self.nombre} | {self.cantidad} | ${self.precio:.2f} | {self.categoria}"

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
            id=data["id"],
            nombre=data["nombre"],
            cantidad=data["cantidad"],
            precio=data["precio"],
            categoria=data.get("categoria", None)
        )
