import tkinter as tk
from tkinter import ttk

# Crear la ventana principal
root = tk.Tk()
root.title("Perfil del Estudiante")
root.geometry("500x400")

# Título principal
title_label = tk.Label(root, text="Perfil del Estudiante", font=("Arial", 20, "bold"))
title_label.pack(pady=20)

# Crear el marco para la tarjeta
card_frame = ttk.Frame(root, padding="10")
card_frame.pack(fill="both", expand=True, padx=20, pady=10)

# Encabezado de la tarjeta
header_frame = ttk.Frame(card_frame)
header_frame.pack(fill="x")

header_title = tk.Label(header_frame, text="Juan Pérez", font=("Arial", 16, "bold"))
header_title.pack(anchor="w")

header_description = tk.Label(header_frame, text="Estudiante de 5to grado", font=("Arial", 12))
header_description.pack(anchor="w")

# Contenido de la tarjeta
content_frame = ttk.Frame(card_frame)
content_frame.pack(fill="both", expand=True)

# Crear la cuadrícula para los detalles del estudiante
details = [
    ("Número de Identificación:", "12345678"),
    ("Fecha de Nacimiento:", "01/01/2010"),
    ("Dirección:", "123 Calle Principal, Cualquier Ciudad, 12345"),
    ("Teléfono:", "(123) 456-7890")
]

for label, value in details:
    row_frame = ttk.Frame(content_frame, padding="5")
    row_frame.pack(fill="x", padx=10, pady=5)

    label_widget = tk.Label(row_frame, text=label, font=("Arial", 12))
    label_widget.pack(side="left")

    value_widget = tk.Label(row_frame, text=value, font=("Arial", 12, "bold"))
    value_widget.pack(side="left", padx=10)

# Iniciar el bucle principal de la interfaz
root.mainloop()
