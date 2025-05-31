import csv
from tkinter import messagebox

def exportar_productos_csv(productos, ruta):
    with open(ruta, mode="w", newline="", encoding="utf-8") as archivo:
        writer = csv.writer(archivo)
        writer.writerow(["ID", "Nombre", "Precio", "Cantidad"])
        for producto in productos:
            writer.writerow([producto.id, producto.nombre, producto.precio, producto.cantidad])

def importar_productos_csv(ruta, callback_actualizar_tabla):
    productos = []
    try:
        with open(ruta, mode='r', newline='', encoding='utf-8') as archivo_csv:
            lector = csv.DictReader(archivo_csv)
            for fila in lector:
                producto = {
                    "id": fila['ID'],
                    "nombre": fila['Nombre'],
                    "cantidad": int(fila['Cantidad']),
                    "precio": float(fila['Precio'])
                }
                productos.append(producto)
        callback_actualizar_tabla()
        return productos
    except FileNotFoundError:
        messagebox.showerror("Error", f"El archivo {ruta} no se encontró.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo importar los productos: {e}")
        return []