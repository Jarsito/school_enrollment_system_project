import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Función para manejar el cambio de DNI
def handle_dni_change(*args):
    dni_var.set(dni_entry.get())

# Función para manejar la eliminación del DNI
def handle_dni_delete():
    dni_var.set("")
    messagebox.showinfo("Eliminar alumno", "Alumno eliminado")

# Crear la ventana principal
root = tk.Tk()
root.title("Eliminar alumno")
root.geometry("400x300")

# Variable para almacenar el DNI
dni_var = tk.StringVar()

# Marco principal de la tarjeta
card_frame = ttk.Frame(root, padding="20", style="Card.TFrame")
card_frame.pack(fill="both", expand=True, padx=20, pady=20)

# Encabezado de la tarjeta
header_frame = ttk.Frame(card_frame, style="Card.TFrame")
header_frame.pack(fill="x")

header_title = tk.Label(header_frame, text="Eliminar alumno", font=("Arial", 16, "bold"))
header_title.pack(anchor="w")

header_description = tk.Label(header_frame, text="Ingresa el DNI del alumno y presiona el botón para eliminarlo.", font=("Arial", 12))
header_description.pack(anchor="w")

# Contenido de la tarjeta
content_frame = ttk.Frame(card_frame, padding="10", style="Card.TFrame")
content_frame.pack(fill="both", expand=True)

# Etiqueta y entrada de DNI
label_dni = tk.Label(content_frame, text="DNI", font=("Arial", 12))
label_dni.pack(anchor="w")

dni_entry = ttk.Entry(content_frame, textvariable=dni_var)
dni_entry.pack(fill="x", pady=10)
dni_var.trace_add("write", handle_dni_change)

# Pie de la tarjeta con el botón
footer_frame = ttk.Frame(card_frame, style="Card.TFrame")
footer_frame.pack(fill="x")

delete_button = ttk.Button(footer_frame, text="Eliminar alumno", command=handle_dni_delete)
delete_button.pack(side="right", pady=10)

# Estilo de marco de tarjeta
style = ttk.Style()
style.configure("Card.TFrame", background="#f0f0f0", borderwidth=2, relief="solid")

# Iniciar el bucle principal de la interfaz
root.mainloop()
