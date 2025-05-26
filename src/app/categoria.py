import uuid

class Categoria:
    def __init__(self, nombre, id=None):
        self.id = id or str(uuid.uuid4())
        self.nombre = nombre


    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            nombre=data["nombre"],
            id=data.get("id")
        )