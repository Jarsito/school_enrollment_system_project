import tkinter as tk
from tkinter import ttk

# Configuración de colores
COLOR_PRINCIPAL = "#007bff"  # Color principal
COLOR_FONDO_TEXTO = "#ffffff"  # Color del texto de fondo

# Crear la ventana principal
root = tk.Tk()
root.title("School Registration System")
root.geometry("800x600")

# Estilo para el encabezado
style = ttk.Style()
style.configure("Header.TFrame", background=COLOR_PRINCIPAL)
style.configure("Header.TLabel", background=COLOR_PRINCIPAL, foreground=COLOR_FONDO_TEXTO)
style.configure("Title.TLabel", font=("Arial", 24, "bold"))
style.configure("Address.TLabel", font=("Arial", 12))

# Crear el marco del encabezado
header_frame = ttk.Frame(root, padding="10", style="Header.TFrame")
header_frame.pack(fill="x")

# Título
title_label = ttk.Label(header_frame, text="I.E Miguel Grau y Seminario", style="Title.TLabel")
title_label.pack(side="left")

# Dirección
address_label = ttk.Label(header_frame, text="El Porvenir del Distrito de Querecotillo, Sullana", style="Address.TLabel")
address_label.pack(side="right")

# Iniciar el bucle principal de la interfaz
root.mainloop()
