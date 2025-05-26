import json
import sys
import os
from app.categoria import Categoria

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

def cargar_categorias(ruta):
    try:
        with open(ruta, "r") as f:
            datos = json.load(f)
            return [Categoria.from_dict(item) for item in datos]
        
    except FileNotFoundError:
        return []
    
def guardar_categorias(ruta, categorias):
    with open(ruta, "w") as f:
        json.dump([c.to_dict() for c in categorias], f, indent=4)

