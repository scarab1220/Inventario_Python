# Inventario de Productos en Python 🗃️

Este es un sistema completo de inventario desarrollado en Python con una interfaz gráfica moderna usando `tkinter`. Permite gestionar productos y categorías, realizar operaciones CRUD, mantener un historial de acciones, y soporta importación/exportación de productos en formato CSV. Todos los datos se guardan de forma persistente en archivos JSON.

## 📌 Funcionalidades

- Crear, visualizar, editar y eliminar productos con ID, nombre, cantidad, precio y categoría
- Gestión de categorías (crear, mostrar, eliminar)
- Visualización de historial de acciones en ventana emergente
- Filtros y ordenamiento en la tabla de productos
- Exportar productos a archivo CSV
- Importar productos desde archivo CSV
- Visualización de totales por categoría (cantidad y suma de precios)
- Guardado automático y persistente en archivos JSON
- Interfaz gráfica amigable y moderna

## 🛠 Requisitos

- Python 3.10 o superior
- Librerías utilizadas:
  - `tkinter` (incluido en Python)
  - `os`
  - `csv`
  - `json`
  - `uuid`
  - `tkinter.messagebox`, `tkinter.simpledialog`, `tkinter.filedialog`

## ▶️ Cómo ejecutar

1. Asegúrate de tener Python instalado
2. Abre la terminal y navega hasta la carpeta `INVENTARIO PROYECTO`
3. Ejecuta el archivo principal:

```bash
python src/main.py
```

## 📁 Estructura del proyecto

```
INVENTARIO PROYECTO/
├── src/
│   ├── main.py
│   ├── app/
│   │   ├── inventario.py
│   │   ├── producto.py
│   │   ├── categoria.py
│   │   ├── historial.py
│   │   └── import_export.py
│   ├── storage/
│   │   ├── storage.py
│   │   ├── categoria_storage.py
│   │   └── historial_storage.py
│   └── ui/
│       └── gui.py
├── data/
│   ├── datos.json
│   ├── categorias.json
│   └── historial.json
├── productos_exportados.csv
├── README.md
└── requirements.txt
```

## ℹ️ Notas

- Los archivos de datos (`datos.json`, `categorias.json`, `historial.json`) se generan y actualizan automáticamente.
- El historial de acciones y las categorías también son persistentes.
- Puedes importar y exportar productos en formato CSV desde la interfaz gráfica.
- El sistema soporta múltiples categorías y muestra totales por cada una.

---

¡Disfruta gestionando tu inventario!