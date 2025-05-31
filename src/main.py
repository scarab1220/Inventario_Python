from app.inventario import Inventario
from storage.storage import JsonStorage
from storage.categoria_storage import cargar_categorias, guardar_categorias
from ui.gui import iniciar_interfaz
from app.historial import Historial
from storage.historial_storage import guardar_historial, cargar_historial

if __name__ == "__main__":
    # Inicializar almacenamiento y cargar datos
    storage = JsonStorage("data/datos.json")
    inventario = Inventario(storage)
    inventario.cargar()
    categorias = cargar_categorias("data/categorias.json")
    inventario.set_categorias(categorias)
    historial = Historial()

    # --- Cargar historial antes de la interfaz ---
    datos_historial = cargar_historial("data/historial.json")
    if isinstance(datos_historial, dict) and "acciones" in datos_historial:
        historial.cargar_desde_lista(datos_historial["acciones"])
    elif isinstance(datos_historial, list):
        historial.cargar_desde_lista(datos_historial)

    # --- Ejecutar interfaz ---
    iniciar_interfaz(inventario, historial)

    # --- Guardar después de la sesión ---
    guardar_categorias("data/categorias.json", inventario.listar_categorias())
    guardar_historial("data/historial.json", historial.to_dict())