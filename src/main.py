from app.inventario import Inventario
from storage.storage import JsonStorage
from storage.categoria_storage import cargar_categorias, guardar_categorias
from ui.gui import iniciar_interfaz
from app.historial import Historial
from storage.historial_storage import guardar_historial, cargar_historial

if __name__ == "__main__":
    storage = JsonStorage("data/datos.json")
    inventario = Inventario(storage)
    inventario.cargar()
    categorias = cargar_categorias("data/categorias.json")
    inventario.set_categorias(categorias)
    historial = Historial()
    iniciar_interfaz(inventario, historial)
    guardar_categorias("data/categorias.json", inventario.listar_categorias())
    historial.cargar_desde_lista(cargar_historial("data/historial.json"))
    guardar_historial("data/historial.json", historial.to_dict())
