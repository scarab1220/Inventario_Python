# src/gui.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

def iniciar_interfaz(inventario, historial):
    root = tk.Tk()
    root.title("Sistema de Inventario")
    root.geometry("900x600")
    root.resizable(True, True)  # Permitir redimensionar la ventana

    # === ESTILO MODERNO ===
    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure("TFrame", background="#e3f0fc")
    style.configure("TLabel", background="#e3f0fc", foreground="#1a3c6b")
    style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=12, background="#4a90e2", foreground="white")
    style.map("TButton",
          background=[("active", "#357ab8")],
          foreground=[("active", "white")])
    style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#4a90e2", foreground="white")
    style.configure("Treeview", font=("Segoe UI", 10), rowheight=28, background="#e3f0fc", fieldbackground="#e3f0fc")
    root.option_add("*Font", ("Segoe UI", 10))
    root.configure(bg="#e3f0fc")

    # === ENCABEZADO PRINCIPAL ===
    header = ttk.Label(root, text="Sistema de Inventario", font=("Segoe UI", 18, "bold"), background="#e3f0fc", foreground="#1a3c6b")
    header.pack(fill="x", padx=10, pady=(10, 0))

    # === VARIABLES DE ENTRADA ===
    nombre_var = tk.StringVar()
    cantidad_var = tk.StringVar()
    precio_var = tk.StringVar()
    producto_seleccionado = [None]
    categoria_var = tk.StringVar()
    filter_var = tk.StringVar()

    # === CINTA DE ACCIONES (RIBBON) ===
    ribbon = ttk.Frame(root, padding=10)
    ribbon.pack(fill="x", padx=10, pady=(10, 0))

    # Acciones de Producto
    product_frame = ttk.LabelFrame(ribbon, text="Acciones de Producto", padding=8)
    product_frame.pack(side="left", padx=5, pady=0)
    ttk.Button(product_frame, text="Crear", command=lambda: crear_producto()).pack(side="left", padx=2)
    ttk.Button(product_frame, text="Actualizar", command=lambda: actualizar_producto()).pack(side="left", padx=2)
    ttk.Button(product_frame, text="Eliminar", command=lambda: eliminar_producto()).pack(side="left", padx=2)
    ttk.Button(product_frame, text="Limpiar", command=lambda: limpiar_campos()).pack(side="left", padx=2)

    # Acciones de Categoría
    category_frame = ttk.LabelFrame(ribbon, text="Acciones de Categoría", padding=8)
    category_frame.pack(side="left", padx=5, pady=0)
    ttk.Button(category_frame, text="Mostrar Categorías", command=lambda: mostrar_categorias()).pack(side="left", padx=2)
    ttk.Button(category_frame, text="Crear Categoría", command=lambda: crear_categoria()).pack(side="left", padx=2)
    ttk.Button(category_frame, text="Eliminar Categoría", command=lambda: eliminar_categoria()).pack(side="left", padx=2)

    # === FILA SUPERIOR: FORMULARIO Y FILTRO ===
    top_row_frame = ttk.Frame(root)
    top_row_frame.pack(fill="x", padx=10, pady=5)

    # Formulario de Producto (izquierda)
    frame_form = ttk.LabelFrame(top_row_frame, text="Datos del producto", padding=10)
    frame_form.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

    ttk.Label(frame_form, text="Nombre:").grid(row=0, column=0, sticky="e", padx=2, pady=2)
    ttk.Entry(frame_form, textvariable=nombre_var, width=30).grid(row=0, column=1, padx=2, pady=2)
    ttk.Label(frame_form, text="Cantidad:").grid(row=1, column=0, sticky="e", padx=2, pady=2)
    ttk.Entry(frame_form, textvariable=cantidad_var, width=10).grid(row=1, column=1, sticky="w", padx=2, pady=2)
    ttk.Label(frame_form, text="Precio:").grid(row=2, column=0, sticky="e", padx=2, pady=2)
    ttk.Entry(frame_form, textvariable=precio_var, width=10).grid(row=2, column=1, sticky="w", padx=2, pady=2)
    ttk.Label(frame_form, text="Categoría:").grid(row=3, column=0, sticky="e", padx=2, pady=2)
    categoria_combo = ttk.Combobox(frame_form, textvariable=categoria_var, state="readonly")
    categoria_combo.grid(row=3, column=1, padx=2, pady=2, sticky="ew")
    frame_form.columnconfigure(1, weight=1)

    # Filtro de Productos (derecha)
    filter_frame = ttk.LabelFrame(top_row_frame, text="Filtrar Productos", padding=8)
    filter_frame.grid(row=0, column=1, sticky="nsew")
    ttk.Label(filter_frame, text="Filtrar:").pack(side="left", padx=2)
    filter_entry = ttk.Entry(filter_frame, textvariable=filter_var, width=15)
    filter_entry.pack(side="left", padx=2)
    ttk.Button(filter_frame, text="Aplicar Filtro", command=lambda: filtrar_tabla()).pack(side="left", padx=2)

    # Hacer que ambas columnas se expandan si la ventana cambia de tamaño
    top_row_frame.columnconfigure(0, weight=1)
    top_row_frame.columnconfigure(1, weight=1)

    # === TABLA DE PRODUCTOS CON BARRAS DE DESPLAZAMIENTO ===
    frame_tabla = ttk.Frame(root)
    frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)

    scrollbar_x = ttk.Scrollbar(frame_tabla, orient="horizontal")
    scrollbar_x.pack(side="bottom", fill="x")

    scrollbar_y = ttk.Scrollbar(frame_tabla, orient="vertical")
    scrollbar_y.pack(side="right", fill="y")

    tabla = ttk.Treeview(
        frame_tabla,
        columns=("ID", "Nombre", "Cantidad", "Precio", "Categoría"),
        show="headings",
        yscrollcommand=scrollbar_y.set,
        xscrollcommand=scrollbar_x.set
    )
    tabla.pack(side="left", fill="both", expand=True)

    scrollbar_y.config(command=tabla.yview)
    scrollbar_x.config(command=tabla.xview)
    tabla.bind("<<TreeviewSelect>>", lambda event: seleccionar_producto(event))

    for col in ("ID", "Nombre", "Cantidad", "Precio", "Categoría"):
        tabla.column(col, width=100, anchor="center", stretch=True)

    # === FUNCIONES CRUD DE PRODUCTO ===
    def crear_producto():
        try:
            nombre = nombre_var.get()
            cantidad = int(cantidad_var.get())
            precio = float(precio_var.get())
            categoria = categoria_var.get()
            if not nombre:
                raise ValueError("Nombre vacío.")
            inventario.agregar(nombre, cantidad, precio, categoria)
            historial.registrar_accion("Crear producto", f"Producto '{nombre}' creado.")
            actualizar_tabla()
            limpiar_campos()
        except ValueError as e:
            messagebox.showerror("Error", f"Datos inválidos: {e}")

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
                historial.registrar_accion("Actualizar producto", f"Producto '{nombre}' actualizado.")
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
            producto = inventario.buscar(id)
            inventario.eliminar(id)
            historial.registrar_accion("Eliminar producto", f"Producto '{producto.nombre}' eliminado.")
            actualizar_tabla()
            limpiar_campos()

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

    def limpiar_campos():
        nombre_var.set("")
        cantidad_var.set("")
        precio_var.set("")
        producto_seleccionado[0] = None
        tabla.selection_remove(tabla.selection())

    def actualizar_tabla():
        tabla.delete(*tabla.get_children())
        for p in inventario.listar():
            tabla.insert(
                "", "end", iid=p.id,
                values=(p.id, p.nombre, p.cantidad, f"${p.precio:.2f}", getattr(p, "categoria", ""))
            )

    # === FUNCIONES CRUD DE CATEGORÍA ===
    def crear_categoria():
        nombre = tk.simpledialog.askstring("Nueva Categoría", "Ingrese el nombre de la categoría:")
        if nombre:
            inventario.agregar_categoria(nombre)
            historial.registrar_accion("Crear categoría", f"Categoría '{nombre}' creada.")
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
                historial.registrar_accion("Eliminar categoría", f"Categoría '{categoria_seleccionada}' eliminada.")
                messagebox.showinfo("Éxito", f"Categoría '{categoria_seleccionada}' eliminada.")
                actualizar_tabla()
                actualizar_categorias_combo()
            else:
                messagebox.showerror("Error", f"No se encontró la categoría '{categoria_seleccionada}'.")

    def mostrar_categorias():
        categorias_str = "\n".join(f"{c.nombre} ({len(getattr(c, 'productos', []))} productos)" for c in inventario.listar_categorias())
        messagebox.showinfo("Categorías", categorias_str if categorias_str else "No hay categorías registradas.")

    def actualizar_categorias_combo():
        categorias = [c.nombre for c in inventario.listar_categorias()]
        categoria_combo['values'] = categorias
        if categorias:
            categoria_combo.current(0)
        else:
            categoria_var.set("")

    # === FUNCIONES DE FILTRO Y ORDENAMIENTO ===
    def filtrar_tabla():
        filtro = filter_var.get().lower()
        tabla.delete(*tabla.get_children())
        for p in inventario.listar():
            if (filtro in p.nombre.lower()) or (filtro in str(getattr(p, "categoria", "")).lower()):
                tabla.insert(
                    "", "end", iid=p.id,
                    values=(p.id, p.nombre, p.cantidad, f"${p.precio:.2f}", getattr(p, "categoria", ""))
                )

    def sort_by_column(col, reverse):
        data = [(tabla.set(child, col), child) for child in tabla.get_children('')]
        try:
            data.sort(key=lambda t: float(t[0].replace('$', '').replace(',', '')), reverse=reverse)
        except ValueError:
            data.sort(reverse=reverse)
        for index, (val, child) in enumerate(data):
            tabla.move(child, '', index)
        tabla.heading(col, command=lambda: sort_by_column(col, not reverse))

    # Habilitar ordenamiento en todas las columnas
    for col in ("ID", "Nombre", "Cantidad", "Precio", "Categoría"):
        tabla.heading(col, text=col, command=lambda _col=col: sort_by_column(_col, False))

    actualizar_tabla()
    actualizar_categorias_combo()
    root.mainloop()
