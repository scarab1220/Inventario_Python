# Inventario de Productos en Python 🗃️

Este es un sistema básico de inventario desarrollado en Python con una interfaz gráfica utilizando `tkinter`. Permite realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) y guarda los datos de manera persistente en un archivo de texto plano.

## 📌 Funcionalidades

- Crear productos con ID, nombre, cantidad y precio
- Visualizar todos los productos
- Editar un producto por su ID
- Eliminar un producto por su ID
- Guardado automático en archivo `datos.txt`
- Interfaz gráfica amigable

## 🛠 Requisitos

- Python 3.10 o superior
- Librerías utilizadas:
  - `tkinter` (incluido en Python)
  - `os`
  - `tkinter.messagebox` y `tkinter.simpledialog`

## ▶️ Cómo ejecutar

1. Asegúrate de tener Python instalado
2. Abre la terminal y navega hasta la carpeta `INVENTARIO PROYECTO`
3. Ejecuta el archivo principal:

```bash
python inventario_gui.py

## 📁 Estructura del proyecto

INVENTARIO PROYECTO/
├── inventario_gui.py
├── datos.txt
├── README.md
├── requirements.txt
└── .gitignore