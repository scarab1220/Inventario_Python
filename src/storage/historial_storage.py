import json

def guardar_historial(ruta, acciones):

    with open(ruta, 'w', encoding='utf-8') as archivo:
        json.dump(acciones, archivo, indent=4, ensure_ascii=False)

def cargar_historial(ruta):
    try:
        with open(ruta, 'r', encoding='utf-8') as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []
    except Exception as e:
        print(f"Error al cargar el historial: {e}")
        return []