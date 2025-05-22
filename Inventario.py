import os

archivo = "datos.txt"
productos = []

# ---------------- CARGA Y GUARDADO ----------------

def cargar_desde_archivo():
    if not os.path.exists(archivo):
        return
    with open(archivo, "r") as f:
        for linea in f:
            partes = linea.strip().split(";")
            if len(partes) == 4:
                producto = {
                    "id": int(partes[0]),
                    "nombre": partes[1],
                    "cantidad": int(partes[2]),
                    "precio": float(partes[3])
                }
                productos.append(producto)

def guardar_en_archivo():
    with open(archivo, "w") as f:
        for p in productos:
            linea = f"{p['id']};{p['nombre']};{p['cantidad']};{p['precio']}\n"
            f.write(linea)

# ---------------- FUNCIONES CRUD ----------------

def crear_producto():
    try:
        id_nuevo = int(input("Ingrese ID del producto: "))
        if any(p["id"] == id_nuevo for p in productos):
            print("Error: El ID ya existe.")
            return
        nombre = input("Ingrese nombre del producto: ")
        cantidad = int(input("Ingrese cantidad: "))
        precio = float(input("Ingrese precio: "))
        nuevo = {"id": id_nuevo, "nombre": nombre, "cantidad": cantidad, "precio": precio}
        productos.append(nuevo)
        guardar_en_archivo()
        print("Producto agregado con éxito.")
    except ValueError:
        print("Error: entrada inválida.")

def mostrar_productos():
    if not productos:
        print("No hay productos registrados.")
    else:
        for p in productos:
            print(f"ID: {p['id']}, Nombre: {p['nombre']}, Cantidad: {p['cantidad']}, Precio: {p['precio']:.2f}")

def actualizar_producto():
    try:
        id_act = int(input("Ingrese ID del producto a actualizar: "))
        for p in productos:
            if p["id"] == id_act:
                p["nombre"] = input("Nuevo nombre: ")
                p["cantidad"] = int(input("Nueva cantidad: "))
                p["precio"] = float(input("Nuevo precio: "))
                guardar_en_archivo()
                print("Producto actualizado.")
                return
        print("Producto no encontrado.")
    except ValueError:
        print("Error: entrada inválida.")

def eliminar_producto():
    try:
        id_elim = int(input("Ingrese ID del producto a eliminar: "))
        for i, p in enumerate(productos):
            if p["id"] == id_elim:
                confirm = input("¿Está seguro de eliminar este producto? (s/n): ").lower()
                if confirm == "s":
                    productos.pop(i)
                    guardar_en_archivo()
                    print("Producto eliminado.")
                return
        print("Producto no encontrado.")
    except ValueError:
        print("Error: entrada inválida.")

# ---------------- MENÚ PRINCIPAL ----------------

def mostrar_menu():
    print("\n===== MENÚ DE INVENTARIO =====")
    print("1. Crear producto")
    print("2. Ver productos")
    print("3. Actualizar producto")
    print("4. Eliminar producto")
    print("5. Salir")

def main():
    cargar_desde_archivo()
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            crear_producto()
        elif opcion == "2":
            mostrar_productos()
        elif opcion == "3":
            actualizar_producto()
        elif opcion == "4":
            eliminar_producto()
        elif opcion == "5":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()
