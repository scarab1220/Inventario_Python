from datetime import datetime

class Historial:
    def __init__(self):
        self.acciones = []

    def registrar_accion(self, accion, descripcion):
        entrada = {
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "accion": accion,
            "descripcion": descripcion
        }
        self.acciones.append(entrada)

    def obtener_historial(self):
        return self.acciones

    def to_dict(self):
        return {
            "acciones": self.acciones
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            nombre=data["nombre"],
            cantidad=int(data["cantidad"]),
            precio=float(data["precio"]),
            categoria=data.get("categoria", "")
        )

    def cargar_desde_lista(self, lista):
        self.acciones = lista

