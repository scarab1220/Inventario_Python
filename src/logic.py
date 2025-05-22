import uuid

def crear_producto(lista, nombre, cantidad, precio):
    producto = {
        "id": str(uuid.uuid4())[:8],
        "nombre": nombre,
        "cantidad": cantidad,
        "precio": precio
    }
    lista.append(producto)

def listar_productos(lista):
    if not lista:
        return "No hay productos."
    texto = ""
    for p in lista:
        texto += f"{p['id']} | {p['nombre']} | {p['cantidad']} | ${p['precio']:.2f}\n"
    return texto

def actualizar_producto(lista, id, nombre, cantidad, precio):
    for p in lista:
        if p['id'] == id:
            p.update({"nombre": nombre, "cantidad": cantidad, "precio": precio})
            return True
    return False

def eliminar_producto(lista, id):
    for i, p in enumerate(lista):
        if p['id'] == id:
            del lista[i]
            return True
    return False
