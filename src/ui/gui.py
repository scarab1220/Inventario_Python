# src/gui.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

def iniciar_interfaz(inventario):
    root = tk.Tk()
    root.title("Sistema de Inventario")
    root.geometry("900x600")  # Wider and taller window
    root.resizable(False, False)

    # Modern style
    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure("TFrame", background="#e3f0fc")
    style.configure("TLabel", background="#e3f0fc", foreground="#1a3c6b")
    style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=8, background="#4a90e2", foreground="white")
    style.map("TButton",
          background=[("active", "#357ab8")],
          foreground=[("active", "white")])
    style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#4a90e2", foreground="white")
    style.configure("Treeview", font=("Segoe UI", 10), rowheight=28, background="#e3f0fc", fieldbackground="#e3f0fc")
    root.option_add("*Font", ("Segoe UI", 10))
    root.configure(bg="#e3f0fc")

    # === Variables de entrada ===
    nombre_var = tk.StringVar()
    cantidad_var = tk.StringVar()
    precio_var = tk.StringVar()
    producto_seleccionado = [None]
    categoria_var = tk.StringVar()

    # === Funciones internas ===
    def actualizar_tabla():
        tabla.delete(*tabla.get_children())
        for p in inventario.listar():
            tabla.insert(
                "", "end", iid=p.id,
                values=(p.id, p.nombre, p.cantidad, f"${p.precio:.2f}", getattr(p, "categoria", ""))
            )

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
            categoria = categoria_var.get()
            if not nombre:
                raise ValueError("Nombre vacío.")
            inventario.agregar(nombre, cantidad, precio, categoria)
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
                categoria_var.set(getattr(producto, "categoria", ""))
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
            categoria = categoria_var.get()
            if not nombre:
                raise ValueError("Nombre vacío.")
            if inventario.actualizar(id, nombre, cantidad, precio, categoria):
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

    def mostrar_categorias():
        categorias_str = "\n".join(f"{c.nombre} ({len(c.productos)} productos)" for c in inventario.listar_categorias())
        messagebox.showinfo("Categorías", categorias_str if categorias_str else "No hay categorías registradas.")

    def crear_categoria():
        nombre = tk.simpledialog.askstring("Nueva Categoría", "Ingrese el nombre de la categoría:")
        if nombre:
            inventario.agregar_categoria(nombre)
            messagebox.showinfo("Éxito", f"Categoría '{nombre}' creada.")
            actualizar_categorias_combo()
        else:
            messagebox.showwarning("Aviso", "Nombre de categoría no puede estar vacío.")

    def eliminar_categoria():
        categorias = inventario.listar_categorias()
        if not categorias:
            messagebox.showwarning("Aviso", "No hay categorías para eliminar.")
            return
        categoria_seleccionada = tk.simpledialog.askstring("Eliminar Categoría", "Ingrese el nombre de la categoría a eliminar:")
        if categoria_seleccionada:
            if inventario.eliminar_categoria(categoria_seleccionada):
                messagebox.showinfo("Éxito", f"Categoría '{categoria_seleccionada}' eliminada.")
                actualizar_tabla()
                actualizar_categorias_combo()
            else:
                messagebox.showerror("Error", f"No se encontró la categoría '{categoria_seleccionada}'.")
    
    def actualizar_categorias_combo():
        categorias = [c.nombre for c in inventario.listar_categorias()]
        categoria_combo['values'] = categorias
        if categorias:
            categoria_combo.current(0)
        else:
            categoria_var.set("")

    # === Layout ===

    frame_form = ttk.LabelFrame(root, text="Datos del producto", padding=10)
    frame_form.pack(fill="x", padx=10, pady=5)

    ttk.Label(frame_form, text="Nombre:").grid(row=0, column=0, sticky="e")
    ttk.Entry(frame_form, textvariable=nombre_var, width=30).grid(row=0, column=1, padx=5)

    ttk.Label(frame_form, text="Cantidad:").grid(row=1, column=0, sticky="e")
    ttk.Entry(frame_form, textvariable=cantidad_var, width=10).grid(row=1, column=1, sticky="w", padx=5)

    ttk.Label(frame_form, text="Precio:").grid(row=2, column=0, sticky="e")
    ttk.Entry(frame_form, textvariable=precio_var, width=10).grid(row=2, column=1, sticky="w", padx=5)

    ttk.Label(frame_form, text="Categoría:").grid(row=3, column=0, sticky="e")
    categoria_combo = ttk.Combobox(frame_form, textvariable=categoria_var, state="readonly", width=28)
    categoria_combo.grid(row=3, column=1, padx=5, pady=2)

    frame_botones = ttk.Frame(root)
    frame_botones.pack(pady=5)

    # Load icons (if you have them, otherwise remove image=... from buttons)
    # icon_crear = tk.PhotoImage(file="icons/add.png")
    # icon_actualizar = tk.PhotoImage(file="icons/update.png")
    # icon_eliminar = tk.PhotoImage(file="icons/delete.png")
    # icon_limpiar = tk.PhotoImage(file="icons/clear.png")
    # icon_mostrar_categorias = tk.PhotoImage(file="icons/categories.png")
    # icon_crear_categoria = tk.PhotoImage(file="icons/add_category.png")
    # icon_eliminar_categoria = tk.PhotoImage(file="icons/delete_category.png")

    # If you don't have icons, use this for your buttons:
    ttk.Button(frame_botones, text="Crear", command=crear_producto).grid(row=0, column=0, padx=5)
    ttk.Button(frame_botones, text="Actualizar", command=actualizar_producto).grid(row=0, column=1, padx=5)
    ttk.Button(frame_botones, text="Eliminar", command=eliminar_producto).grid(row=0, column=2, padx=5)
    ttk.Button(frame_botones, text="Limpiar", command=limpiar_campos).grid(row=0, column=3, padx=5)
    ttk.Button(frame_botones, text="Mostrar Categorías", command=mostrar_categorias).grid(row=0, column=4, padx=5)
    ttk.Button(frame_botones, text="Crear Categoría", command=crear_categoria).grid(row=0, column=5, padx=5)
    ttk.Button(frame_botones, text="Eliminar Categoría", command=eliminar_categoria).grid(row=0, column=6, padx=5)

    tabla = ttk.Treeview(root, columns=("ID", "Nombre", "Cantidad", "Precio", "Categoría"), show="headings")
    tabla.heading("ID", text="ID")
    tabla.heading("Nombre", text="Nombre")
    tabla.heading("Cantidad", text="Cantidad")
    tabla.heading("Precio", text="Precio")
    tabla.heading("Categoría", text="Categoría")
    tabla.pack(fill="both", expand=True, padx=10, pady=10)
    tabla.bind("<<TreeviewSelect>>", seleccionar_producto)

    def on_enter(e):
        e.widget['style'] = 'Hover.TButton'

    def on_leave(e):
        e.widget['style'] = 'TButton'


    for child in frame_botones.winfo_children():
        child.bind("<Enter>", on_enter)
        child.bind("<Leave>", on_leave)

    actualizar_tabla()
    actualizar_categorias_combo()
    root.mainloop()
