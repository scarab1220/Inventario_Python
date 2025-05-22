# src/gui.py
import tkinter as tk
from tkinter import ttk, messagebox
from producto import Producto

def iniciar_interfaz(inventario):
    root = tk.Tk()
    root.title("Sistema de Inventario")
    root.geometry("700x500")
    root.resizable(False, False)

    # === Variables de entrada ===
    nombre_var = tk.StringVar()
    cantidad_var = tk.StringVar()
    precio_var = tk.StringVar()
    producto_seleccionado = [None]

    # === Funciones internas ===
    def actualizar_tabla():
        tabla.delete(*tabla.get_children())
        for p in inventario.listar():
            tabla.insert("", "end", iid=p.id, values=(p.id, p.nombre, p.cantidad, f"${p.precio:.2f}"))

    def limpiar_campos():
        nombre_var.set("")
        cantidad_var.set("")
        precio_var.set("")
        producto_seleccionado[0] = None
        tabla.selection_remove(tabla.selection())

    def crear_producto():
        try:
            nombre = nombre_var.get()
            cantidad = int(cantidad_var.get())
            precio = float(precio_var.get())
            if not nombre:
                raise ValueError("Nombre vacío.")
            inventario.agregar(nombre, cantidad, precio)
            actualizar_tabla()
            limpiar_campos()
        except ValueError as e:
            messagebox.showerror("Error", f"Datos inválidos: {e}")

    def seleccionar_producto(event):
        selected = tabla.focus()
        if selected:
            producto = inventario.buscar(selected)
            if producto:
                nombre_var.set(producto.nombre)
                cantidad_var.set(str(producto.cantidad))
                precio_var.set(str(producto.precio))
                producto_seleccionado[0] = producto.id

    def actualizar_producto():
        if not producto_seleccionado[0]:
            messagebox.showwarning("Aviso", "Selecciona un producto.")
            return
        try:
            id = producto_seleccionado[0]
            nombre = nombre_var.get()
            cantidad = int(cantidad_var.get())
            precio = float(precio_var.get())
            if not nombre:
                raise ValueError("Nombre vacío.")
            if inventario.actualizar(id, nombre, cantidad, precio):
                actualizar_tabla()
                limpiar_campos()
            else:
                messagebox.showerror("Error", "No se encontró el producto.")
        except ValueError as e:
            messagebox.showerror("Error", f"Datos inválidos: {e}")

    def eliminar_producto():
        id = producto_seleccionado[0]
        if not id:
            messagebox.showwarning("Aviso", "Selecciona un producto.")
            return
        confirm = messagebox.askyesno("Confirmar", "¿Eliminar este producto?")
        if confirm:
            inventario.eliminar(id)
            actualizar_tabla()
            limpiar_campos()

    # === Layout ===

    frame_form = ttk.LabelFrame(root, text="Datos del producto", padding=10)
    frame_form.pack(fill="x", padx=10, pady=5)

    ttk.Label(frame_form, text="Nombre:").grid(row=0, column=0, sticky="e")
    ttk.Entry(frame_form, textvariable=nombre_var, width=30).grid(row=0, column=1, padx=5)

    ttk.Label(frame_form, text="Cantidad:").grid(row=1, column=0, sticky="e")
    ttk.Entry(frame_form, textvariable=cantidad_var, width=10).grid(row=1, column=1, sticky="w", padx=5)

    ttk.Label(frame_form, text="Precio:").grid(row=2, column=0, sticky="e")
    ttk.Entry(frame_form, textvariable=precio_var, width=10).grid(row=2, column=1, sticky="w", padx=5)

    frame_botones = ttk.Frame(root)
    frame_botones.pack(pady=5)

    ttk.Button(frame_botones, text="Crear", command=crear_producto).grid(row=0, column=0, padx=5)
    ttk.Button(frame_botones, text="Actualizar", command=actualizar_producto).grid(row=0, column=1, padx=5)
    ttk.Button(frame_botones, text="Eliminar", command=eliminar_producto).grid(row=0, column=2, padx=5)
    ttk.Button(frame_botones, text="Limpiar", command=limpiar_campos).grid(row=0, column=3, padx=5)

    tabla = ttk.Treeview(root, columns=("ID", "Nombre", "Cantidad", "Precio"), show="headings")
    tabla.heading("ID", text="ID")
    tabla.heading("Nombre", text="Nombre")
    tabla.heading("Cantidad", text="Cantidad")
    tabla.heading("Precio", text="Precio")
    tabla.pack(fill="both", expand=True, padx=10, pady=10)
    tabla.bind("<<TreeviewSelect>>", seleccionar_producto)

    actualizar_tabla()
    root.mainloop()
