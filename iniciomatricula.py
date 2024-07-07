import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def iniciar_sesion():
    messagebox.showinfo("Inicio de Sesión", "Iniciar sesión presionado")

def matricular():
    messagebox.showinfo("Matrícula", "Matricular presionado")

def mostrar_mensaje(mensaje):
    messagebox.showinfo("Mensaje", mensaje)

# Crear la ventana principal
root = tk.Tk()
root.title("Sistema de Matrícula Escolar")
root.geometry("800x600")

# Marco principal
main_frame = ttk.Frame(root, padding="20")
main_frame.pack(fill="both", expand=True)

# Título y descripción
title_label = tk.Label(main_frame, text="Bienvenido al Sistema de Matrícula Escolar", font=("Arial", 24, "bold"))
title_label.pack(pady=20)

description_label = tk.Label(main_frame, text="Inicia sesión para acceder a tu cuenta.", font=("Arial", 12))
description_label.pack(pady=10)

# Estilo de marco de tarjeta
style = ttk.Style()
style.configure("Card.TFrame", background="#f0f0f0", borderwidth=2, relief="solid")
style.configure("Card.TLabel", background="#f0f0f0")

# Crear un marco para los cuadros de inicio de sesión y matrícula
login_matricula_frame = ttk.Frame(main_frame)
login_matricula_frame.pack(fill="x", expand=True, pady=20)

# Cuadro de entrada para iniciar sesión
login_frame = ttk.Frame(login_matricula_frame, padding="20", style="Card.TFrame")
login_frame.pack(side="left", fill="both", expand=True, padx=10)

# Usuario
user_label = tk.Label(login_frame, text="Usuario", font=("Arial", 12), bg="#f0f0f0")
user_label.grid(row=0, column=0, sticky="w", pady=5)
user_entry = ttk.Entry(login_frame)
user_entry.grid(row=0, column=1, pady=5)

# Contraseña
password_label = tk.Label(login_frame, text="Contraseña", font=("Arial", 12), bg="#f0f0f0")
password_label.grid(row=1, column=0, sticky="w", pady=5)
password_entry = ttk.Entry(login_frame, show="*")
password_entry.grid(row=1, column=1, pady=5)

# Botón de iniciar sesión
login_button = ttk.Button(login_frame, text="Iniciar Sesión", command=iniciar_sesion)
login_button.grid(row=2, column=0, columnspan=2, pady=10)

# Enlace de "Olvidaste tu contraseña"
forgot_password_label = tk.Label(login_frame, text="¿Olvidaste tu contraseña?", font=("Arial", 10), fg="blue", cursor="hand2", bg="#f0f0f0")
forgot_password_label.grid(row=3, column=0, columnspan=2, pady=5)
forgot_password_label.bind("<Button-1>", lambda e: mostrar_mensaje("Enlace de recuperación de contraseña presionado"))

# Cuadro de matrícula
matricula_frame = ttk.Frame(login_matricula_frame, padding="20", style="Card.TFrame")
matricula_frame.pack(side="right", fill="both", expand=True, padx=10)

# Título y descripción de matrícula
matricula_title = tk.Label(matricula_frame, text="Matricular", font=("Arial", 18, "bold"), bg="#f0f0f0")
matricula_title.pack(pady=10)

matricula_description = tk.Label(matricula_frame, text="Haz clic en el botón para iniciar el proceso de matrícula.", font=("Arial", 12), bg="#f0f0f0")
matricula_description.pack(pady=5)

# Botón de matrícula
matricula_button = ttk.Button(matricula_frame, text="Matricular", command=matricular)
matricula_button.pack(pady=10)

# Iniciar el bucle principal de la interfaz
root.mainloop()
