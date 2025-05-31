# src/gui.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
from app.import_export import exportar_productos_csv, importar_productos_csv

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

    # === FUNCIONES CRUD DE PRODUCTO ===
    def crear_producto():
        nombre = nombre_var.get().strip()
        cantidad = cantidad_var.get().strip()
        precio = precio_var.get().strip()
        categoria = categoria_var.get().strip()

        # Validaciones amigables
        if not nombre:
            messagebox.showwarning("Campo requerido", "Por favor ingresa el nombre del producto.")
            return
        if not cantidad:
            messagebox.showwarning("Campo requerido", "Por favor ingresa la cantidad.")
            return
        if not precio:
            messagebox.showwarning("Campo requerido", "Por favor ingresa el precio.")
            return
        if not categoria:
            messagebox.showwarning("Campo requerido", "Por favor selecciona una categoría.")
            return

        try:
            cantidad = int(cantidad)
            precio = float(precio)
        except ValueError:
            messagebox.showerror("Error de formato", "Cantidad debe ser un número entero y precio un número decimal.")
            return

        inventario.agregar(nombre, cantidad, precio, categoria)
        historial.registrar_accion("Crear producto", f"Producto '{nombre}' creado.")
        actualizar_tabla()
        limpiar_campos()
        messagebox.showinfo("Éxito", f"Producto '{nombre}' creado correctamente.")

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
                values=(p.id, p.nombre, p.cantidad, f"${float(p.precio):.2f}", getattr(p, "categoria", ""))
            )
    
    def manejar_exportacion():
        productos = inventario.listar()
        exportar_productos_csv(productos, "productos_exportados.csv")
        messagebox.showinfo("Exportación exitosa", "Productos exportados a productos_exportados.csv")

    # === NUEVA FUNCIÓN PARA IMPORTAR DESDE CSV ===
    def manejar_importacion():
        ruta = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv"), ("Todos los archivos", "*")]
        )
        if ruta:
            productos = importar_productos_csv(ruta, lambda: None)  # No actualiza tabla aquí
            if productos:
                for p in productos:
                    inventario.agregar(p["nombre"], p["cantidad"], p["precio"], p.get("categoria", ""))
                actualizar_tabla()
                messagebox.showinfo("Importación exitosa", f"Se importaron {len(productos)} productos.")

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
        ventana_categorias = tk.Toplevel(root)
        ventana_categorias.title("Categorías")
        ventana_categorias.geometry("520x350")

        # Frame para la tabla y el scrollbar
        frame_tabla = ttk.Frame(ventana_categorias)
        frame_tabla.pack(fill="both", expand=True)

        tree = ttk.Treeview(frame_tabla, columns=("ID", "Nombre", "Productos", "Total Precio"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Nombre", text="Nombre")
        tree.heading("Productos", text="Productos")
        tree.heading("Total Precio", text="Total Precio")
        tree.pack(side="left", fill="both", expand=True)

        # Scrollbar vertical correctamente asociado
        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        productos = inventario.listar()
        for c in inventario.listar_categorias():
            productos_categoria = [p for p in productos if getattr(p, "categoria", "") == c.nombre]
            total_productos = sum(getattr(p, "cantidad", 0) for p in productos_categoria)
            total_precio = sum(getattr(p, "precio", 0) * getattr(p, "cantidad", 0) for p in productos_categoria)
            tree.insert(
                "", "end",
                values=(
                    getattr(c, "id", ""),
                    c.nombre,
                    total_productos,
                    f"${total_precio:.2f}"
                )
            )

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

    # === FUNCIÓN PARA MOSTRAR EL HISTORIAL ===
    def mostrar_historial():
        ventana_historial = tk.Toplevel(root)
        ventana_historial.title("Historial de acciones")
        ventana_historial.geometry("600x400")
        tree = ttk.Treeview(ventana_historial, columns=("Fecha", "Acción", "Descripción"), show="headings")
        tree.heading("Fecha", text="Fecha")
        tree.heading("Acción", text="Acción")
        tree.heading("Descripción", text="Descripción")
        tree.pack(fill="both", expand=True)

        # Scrollbar vertical
        scrollbar = ttk.Scrollbar(ventana_historial, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        for accion in historial.obtener_historial():
            tree.insert("", "end", values=(accion["fecha"], accion["accion"], accion["descripcion"]))

    # === CINTA DE ACCIONES (RIBBON) ===
    ribbon = ttk.Frame(root, padding=10)
    ribbon.pack(fill="x", padx=10, pady=(10, 0))

    # Acciones de Producto
    product_frame = ttk.LabelFrame(ribbon, text="Acciones de Producto", padding=8)
    product_frame.pack(side="left", padx=5, pady=0)
    ttk.Button(product_frame, text="Crear", command=crear_producto).pack(side="left", padx=2)
    ttk.Button(product_frame, text="Actualizar", command=actualizar_producto).pack(side="left", padx=2)
    ttk.Button(product_frame, text="Eliminar", command=eliminar_producto).pack(side="left", padx=2)
    ttk.Button(product_frame, text="Limpiar", command=limpiar_campos).pack(side="left", padx=2)

    # Acciones de Categoría
    category_frame = ttk.LabelFrame(ribbon, text="Acciones de Categoría", padding=8)
    category_frame.pack(side="left", padx=5, pady=0)
    ttk.Button(category_frame, text="Mostrar Categorías", command=mostrar_categorias).pack(side="left", padx=2)
    ttk.Button(category_frame, text="Crear Categoría", command=crear_categoria).pack(side="left", padx=2)
    ttk.Button(category_frame, text="Eliminar Categoría", command=eliminar_categoria).pack(side="left", padx=2)

    # Historial
    history_frame = ttk.LabelFrame(ribbon, text="Historial", padding=8)
    history_frame.pack(side="left", padx=5, pady=0)
    ttk.Button(history_frame, text="Ver Historial", command=mostrar_historial).pack(side="left", padx=2)

    # === FILA SUPERIOR: FORMULARIO Y FILTRO ===
    top_row_frame = ttk.Frame(root)
    top_row_frame.pack(fill="x", padx=10, pady=5)

    # Formulario de Producto (izquierda)
    frame_form = ttk.LabelFrame(top_row_frame, text="Datos del producto", padding=10)
    frame_form.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

    ttk.Label(frame_form, text="Nombre:").grid(row=0, column=0, sticky="e", padx=2, pady=2)
    ttk.Entry(frame_form, textvariable=nombre_var, width=30).grid(row=0, column=1, padx=2, pady=2, sticky="ew")
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
    ttk.Button(filter_frame, text="Aplicar Filtro", command=filtrar_tabla).pack(side="left", padx=2)
    ttk.Button(filter_frame, text="Exportar a CSV", command=manejar_exportacion).pack(side="left", padx=2)
    ttk.Button(filter_frame, text="Importar desde CSV", command=manejar_importacion).pack(side="left", padx=2)

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

    # Habilitar ordenamiento en todas las columnas
    for col in ("ID", "Nombre", "Cantidad", "Precio", "Categoría"):
        tabla.heading(col, text=col, command=lambda _col=col: sort_by_column(_col, False))

    actualizar_tabla()
    actualizar_categorias_combo()
    root.mainloop()