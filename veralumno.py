import tkinter as tk
from tkinter import ttk

# Crear la ventana principal
root = tk.Tk()
root.title("Alumnos Matriculados")
root.geometry("600x400")

# Estilo de marco de tarjeta
style = ttk.Style()
style.configure("Card.TFrame", background="#f0f0f0", borderwidth=2, relief="solid")
style.configure("Card.TLabel", background="#f0f0f0")
style.configure("Card.Header.TLabel", font=("Arial", 16, "bold"))
style.configure("Card.Description.TLabel", font=("Arial", 12))
style.configure("Table.TFrame", background="#ffffff", borderwidth=1, relief="solid")
style.configure("Table.TLabel", font=("Arial", 12), background="#ffffff")

# Marco principal de la tarjeta
card_frame = ttk.Frame(root, padding="20", style="Card.TFrame")
card_frame.pack(fill="both", expand=True, padx=20, pady=20)

# Encabezado de la tarjeta
header_frame = ttk.Frame(card_frame, style="Card.TFrame")
header_frame.pack(fill="x")

header_title = ttk.Label(header_frame, text="Alumnos Matriculados", style="Card.Header.TLabel")
header_title.pack(anchor="w")

header_description = ttk.Label(header_frame, text="Esta tabla muestra los alumnos actualmente matriculados.", style="Card.Description.TLabel")
header_description.pack(anchor="w")

# Contenido de la tarjeta
content_frame = ttk.Frame(card_frame, padding="10", style="Card.TFrame")
content_frame.pack(fill="both", expand=True)

# Tabla
table_frame = ttk.Frame(content_frame, style="Table.TFrame")
table_frame.pack(fill="both", expand=True)

# Encabezados de la tabla
table_header_frame = ttk.Frame(table_frame, style="Table.TFrame")
table_header_frame.pack(fill="x")

header_name = ttk.Label(table_header_frame, text="Nombre", style="Table.TLabel")
header_name.grid(row=0, column=0, padx=10, pady=5)

header_dni = ttk.Label(table_header_frame, text="DNI", style="Table.TLabel")
header_dni.grid(row=0, column=1, padx=10, pady=5)

# Datos de la tabla
students = [
    ("Sofía Martínez", "12345678A"),
    ("Alejandro Gómez", "87654321B"),
    ("Lucía Fernández", "98765432C"),
    ("Miguel Sánchez", "54321678D"),
    ("Marta Rodríguez", "76543219E")
]

for i, (name, dni) in enumerate(students, start=1):
    row_frame = ttk.Frame(table_frame, style="Table.TFrame")
    row_frame.pack(fill="x")
    
    name_label = ttk.Label(row_frame, text=name, style="Table.TLabel")
    name_label.grid(row=i, column=0, padx=10, pady=5)

    dni_label = ttk.Label(row_frame, text=dni, style="Table.TLabel")
    dni_label.grid(row=i, column=1, padx=10, pady=5)

# Iniciar el bucle principal de la interfaz
root.mainloop()
