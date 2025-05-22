import tkinter as tk
from tkinter import messagebox, simpledialog
from logic import crear_producto, listar_productos, actualizar_producto, eliminar_producto
from storage import guardar_datos

def iniciar_interfaz(inventario):
    def agregar():
        nombre = simpledialog.askstring("Nombre", "Nombre del producto:")
        cantidad = simpledialog.askinteger("Cantidad", "Cantidad:")
        precio = simpledialog.askfloat("Precio", "Precio:")
        crear_producto(inventario, nombre, cantidad, precio)
        guardar_datos("data/datos.txt", inventario)
        messagebox.showinfo("Listo", "Producto agregado.")

    def mostrar():
        texto = listar_productos(inventario)
        messagebox.showinfo("Inventario", texto)

    def editar():
        id = simpledialog.askstring("ID", "ID del producto a editar:")
        nuevo_nombre = simpledialog.askstring("Nuevo nombre", "Nuevo nombre:")
        nueva_cantidad = simpledialog.askinteger("Cantidad", "Nueva cantidad:")
        nuevo_precio = simpledialog.askfloat("Precio", "Nuevo precio:")
        if actualizar_producto(inventario, id, nuevo_nombre, nueva_cantidad, nuevo_precio):
            guardar_datos("data/datos.txt", inventario)
            messagebox.showinfo("Éxito", "Producto actualizado.")
        else:
            messagebox.showerror("Error", "Producto no encontrado.")

    def eliminar():
        id = simpledialog.askstring("Eliminar", "ID del producto:")
        if eliminar_producto(inventario, id):
            guardar_datos("data/datos.txt", inventario)
            messagebox.showinfo("Éxito", "Producto eliminado.")
        else:
            messagebox.showerror("Error", "Producto no encontrado.")

    app = tk.Tk()
    app.title("Inventario")
    tk.Button(app, text="Agregar", command=agregar).pack(fill='x')
    tk.Button(app, text="Mostrar", command=mostrar).pack(fill='x')
    tk.Button(app, text="Editar", command=editar).pack(fill='x')
    tk.Button(app, text="Eliminar", command=eliminar).pack(fill='x')
    tk.Button(app, text="Salir", command=app.quit).pack(fill='x')
    app.mainloop()
