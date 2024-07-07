import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import uuid
from datetime import datetime
from typing import List

# Configuración de colores
COLOR_PRINCIPAL = "#F0E68C"  # Color principal
COLOR_FONDO = "#F0E68C"  # Color de fondo
COLOR_FONDO_TEXTO = "#000000"  # Color del texto de fondo

# Constantes
BASE_DATOS = "base_matricula.db"

class SistemaMatriculas:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.geometry("800x600")
        self.root.title("Sistema de Matrículas Escolares")
        self.root.configure(bg=COLOR_FONDO)

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TFrame", background=COLOR_FONDO)
        self.style.configure("TLabel", background=COLOR_FONDO, font=("Helvetica", 12))
        self.style.configure("TButton", background=COLOR_FONDO, font=("Helvetica", 12, "bold"), padding=6)
        self.style.configure("TEntry", padding=6, font=("Helvetica", 12))
        
        # Configuración de estilos para el encabezado
        self.style.configure("Header.TFrame", background=COLOR_PRINCIPAL)
        self.style.configure("Header.TLabel", background=COLOR_PRINCIPAL, foreground=COLOR_FONDO_TEXTO)
        self.style.configure("Title.TLabel", font=("Arial", 24, "bold"))
        self.style.configure("Address.TLabel", font=("Arial", 12))

        # Crear el marco del encabezado
        header_frame = ttk.Frame(root, padding="10", style="Header.TFrame")
        header_frame.pack(fill="x")

        # Título
        title_label = ttk.Label(header_frame, text="I.E Miguel Grau y Seminario", style="Title.TLabel")
        title_label.pack(side="left")

        # Dirección
        address_label = ttk.Label(header_frame, text="El Porvenir del Distrito de Querecotillo, Sullana", style="Address.TLabel")
        address_label.pack(side="right")

        self.iniciar_sesion_frame = ttk.Frame(root, padding="20", style="Card.TFrame")
        self.iniciar_sesion_frame.pack(side="left", fill="both", expand=True, padx=10, pady=20)

        self.matricula_frame = ttk.Frame(root, padding="20", style="Card.TFrame")
        self.matricula_frame.pack(side="right", fill="both", expand=True, padx=10, pady=20)

        # Formulario de inicio de sesión
        user_label = tk.Label(self.iniciar_sesion_frame, text="Usuario", font=("Arial", 12), bg=COLOR_FONDO)
        user_label.grid(row=0, column=0, sticky="w", pady=5)
        self.user_entry = ttk.Entry(self.iniciar_sesion_frame)
        self.user_entry.grid(row=0, column=1, pady=5)

        password_label = tk.Label(self.iniciar_sesion_frame, text="Contraseña", font=("Arial", 12), bg=COLOR_FONDO)
        password_label.grid(row=1, column=0, sticky="w", pady=5)
        self.password_entry = ttk.Entry(self.iniciar_sesion_frame, show="*")
        self.password_entry.grid(row=1, column=1, pady=5)

        login_button = ttk.Button(self.iniciar_sesion_frame, text="Iniciar Sesión", command=self.iniciar_sesion)
        login_button.grid(row=2, column=0, columnspan=2, pady=10)

        forgot_password_label = tk.Label(self.iniciar_sesion_frame, text="¿Olvidaste tu contraseña?", font=("Arial", 10), fg="blue", cursor="hand2", bg=COLOR_FONDO)
        forgot_password_label.grid(row=3, column=0, columnspan=2, pady=5)
        forgot_password_label.bind("<Button-1>", lambda e: self.mostrar_mensaje("Enlace de recuperación de contraseña presionado"))

        # Formulario de matrícula
        matricula_title = tk.Label(self.matricula_frame, text="Matricular Alumno", font=("Arial", 18, "bold"), bg=COLOR_FONDO)
        matricula_title.pack(pady=10)

        matricula_description = tk.Label(self.matricula_frame, text="Haz clic en el botón para iniciar el proceso de matrícula.", font=("Arial", 12), bg=COLOR_FONDO)
        matricula_description.pack(pady=5)

        matricula_button = ttk.Button(self.matricula_frame, text="Matricular", command=self.matricula)
        matricula_button.pack(pady=10)

        self.inicializar_base_datos()

    def iniciar_sesion(self):
        messagebox.showinfo("Inicio de Sesión", "Iniciar sesión presionado")
        self.iniciar_sesion_frame.pack_forget()
        self.matricula_frame.pack_forget()
        self.mostrar_opciones_principales()

    def mostrar_opciones_principales(self):
        self.seccion_botones = ttk.Frame(self.root, padding="20")
        self.seccion_botones.pack(pady=20, expand=True)

        self.button1 = ttk.Button(self.seccion_botones, text="Matricular Alumno", command=self.matricula, width=20)
        self.button1.pack(side=tk.LEFT, padx=10)

        self.button2 = ttk.Button(self.seccion_botones, text="Ver Base de Alumnos", command=self.mostrar_alumnos, width=20)
        self.button2.pack(side=tk.LEFT, padx=10)

        self.button3 = ttk.Button(self.seccion_botones, text="Buscar Alumno", command=self.buscar_alumno, width=20)
        self.button3.pack(side=tk.LEFT, padx=10)

        self.button4 = ttk.Button(self.seccion_botones, text="Eliminar Alumno", command=self.eliminar_alumno, width=20)
        self.button4.pack(side=tk.LEFT, padx=10)

    def inicializar_base_datos(self):
        conexion = sqlite3.connect(BASE_DATOS)
        cursor = conexion.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alumnos (
                id TEXT PRIMARY KEY,
                nombre TEXT,
                apellido TEXT,
                dni TEXT UNIQUE,
                fecha_nacimiento TEXT,
                nombre_padre TEXT,
                direccion TEXT,
                telefono_padre TEXT,
                hora_matricula TEXT
            )
        ''')
        conexion.commit()
        conexion.close()

    def guardar_datos(self, datos: List[str]) -> bool:
        try:
            conexion = sqlite3.connect(BASE_DATOS)
            cursor = conexion.cursor()
            cursor.execute('''
                INSERT INTO alumnos (id, nombre, apellido, dni, fecha_nacimiento, nombre_padre, direccion, telefono_padre, hora_matricula)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', datos)
            conexion.commit()
            conexion.close()
            return True
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "El DNI ya está registrado.")
            return False
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar los datos: {e}")
            return False

    def validar_dni(self, dni: str) -> bool:
        return len(dni) == 8 and dni.isdigit()

    def validar_campos(self, campos: List[str]) -> bool:
        for campo in campos:
            if not campo:
                return False
        return self.validar_dni(campos[2])

    def accion_matricula(self, nombre_var, apellido_var, dni_var, fecha_nacimiento_var, nombre_padre_var, direccion_var, telefono_padre_var, detalles_frame):
        id_unico = str(uuid.uuid4())
        hora_matricula = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        datos = [
            id_unico, nombre_var.get(), apellido_var.get(), dni_var.get(), fecha_nacimiento_var.get(),
            nombre_padre_var.get(), direccion_var.get(), telefono_padre_var.get(), hora_matricula
        ]

        if not self.validar_campos(datos[1:8]):
            messagebox.showerror("Error", "Todos los campos son obligatorios y el DNI debe tener 8 dígitos.")
            return

        if self.guardar_datos(datos):
            messagebox.showinfo("Matriculación Exitosa", "El alumno se ha matriculado correctamente.")
            self.mostrar_detalles_matricula(detalles_frame, id_unico, apellido_var.get(), hora_matricula)
            self.limpiar_campos([nombre_var, apellido_var, dni_var, fecha_nacimiento_var, nombre_padre_var, direccion_var, telefono_padre_var])

    def crear_entrada(self, ventana: ttk.Frame, texto: str, variable: tk.StringVar, fila: int, columna: int) -> ttk.Entry:
        label = ttk.Label(ventana, text=texto)
        label.grid(row=fila, column=columna, padx=10, pady=5, sticky="E")
        entry = ttk.Entry(ventana, width=40, textvariable=variable)
        entry.grid(row=fila, column=columna+1, padx=10, pady=5)
        return entry

    def limpiar_campos(self, campos: List[tk.StringVar]) -> None:
        for campo in campos:
            campo.set("")

    def mostrar_detalles_matricula(self, frame, id_unico: str, apellido: str, hora_matricula: str) -> None:
        for widget in frame.winfo_children():
            widget.destroy()

        ttk.Label(frame, text=f"ID: {id_unico}", font=("Helvetica", 12)).pack(pady=5)
        ttk.Label(frame, text=f"Apellido: {apellido}", font=("Helvetica", 12)).pack(pady=5)
        ttk.Label(frame, text=f"Hora de Matrícula: {hora_matricula}", font=("Helvetica", 12)).pack(pady=5)

    def matricula(self) -> None:
        ventana_matricula = tk.Toplevel()
        ventana_matricula.geometry("600x700")
        ventana_matricula.title("Sección de Matrícula")
        ventana_matricula.configure(bg=COLOR_FONDO)

        nombre_var = tk.StringVar()
        apellido_var = tk.StringVar()
        dni_var = tk.StringVar()
        fecha_nacimiento_var = tk.StringVar()
        nombre_padre_var = tk.StringVar()
        direccion_var = tk.StringVar()
        telefono_padre_var = tk.StringVar()

        ttk.Label(ventana_matricula, text="Estás en la sección de matrículas", font=("Helvetica", 16, "bold")).pack(pady=(20, 10))

        formulario = ttk.Frame(ventana_matricula)
        formulario.pack(pady=20)

        self.crear_entrada(formulario, "Nombre del alumno:", nombre_var, 0, 0)
        self.crear_entrada(formulario, "Apellido del alumno:", apellido_var, 1, 0)
        self.crear_entrada(formulario, "DNI del alumno:", dni_var, 2, 0)
        self.crear_entrada(formulario, "Fecha de nacimiento:", fecha_nacimiento_var, 3, 0)
        self.crear_entrada(formulario, "Nombre del padre o apoderado:", nombre_padre_var, 4, 0)
        self.crear_entrada(formulario, "Dirección:", direccion_var, 5, 0)
        self.crear_entrada(formulario, "Teléfono del apoderado:", telefono_padre_var, 6, 0)

        detalles_frame = ttk.Frame(ventana_matricula)
        detalles_frame.pack(pady=20)

        ttk.Button(
            ventana_matricula, text="Registrar alumno",
            command=lambda: self.accion_matricula(
                nombre_var, apellido_var, dni_var, fecha_nacimiento_var, nombre_padre_var,
                direccion_var, telefono_padre_var, detalles_frame)
        ).pack(pady=20)

    def mostrar_alumnos(self) -> None:
        ventana_base = tk.Toplevel(self.root)
        ventana_base.geometry("600x500")
        ventana_base.title("Sección base de alumnos")
        ventana_base.configure(bg=COLOR_FONDO)

        style = ttk.Style()
        style.configure("Card.TFrame", background="#F0E68C", borderwidth=2, relief="solid")
        style.configure("Card.TLabel", background="#F0E68C")
        style.configure("Card.Header.TLabel", font=("Arial", 16, "bold"))
        style.configure("Card.Description.TLabel", font=("Arial", 12))
        style.configure("Table.TFrame", background="#F0E68C", borderwidth=1, relief="solid")
        style.configure("Table.TLabel", font=("Arial", 12), background="#F0E68C")

        card_frame = ttk.Frame(ventana_base, padding="20", style="Card.TFrame")
        card_frame.pack(fill="both", expand=True, padx=20, pady=20)

        header_frame = ttk.Frame(card_frame, style="Card.TFrame")
        header_frame.pack(fill="x")

        header_title = ttk.Label(header_frame, text="Alumnos Matriculados", style="Card.Header.TLabel")
        header_title.pack(anchor="w")

        header_description = ttk.Label(header_frame, text="Esta tabla muestra los alumnos actualmente matriculados.", style="Card.Description.TLabel")
        header_description.pack(anchor="w")

        content_frame = ttk.Frame(card_frame, padding="10", style="Card.TFrame")
        content_frame.pack(fill="both", expand=True)

        table_frame = ttk.Frame(content_frame, style="Table.TFrame")
        table_frame.pack(fill="both", expand=True)

        table_header_frame = ttk.Frame(table_frame, style="Table.TFrame")
        table_header_frame.pack(fill="x")

        header_name = ttk.Label(table_header_frame, text="Nombre", style="Table.TLabel")
        header_name.grid(row=0, column=0, padx=10, pady=5)

        header_dni = ttk.Label(table_header_frame, text="DNI", style="Table.TLabel")
        header_dni.grid(row=0, column=1, padx=10, pady=5)

        try:
            conexion = sqlite3.connect(BASE_DATOS)
            cursor = conexion.cursor()
            cursor.execute("SELECT nombre, dni FROM alumnos")
            registros = cursor.fetchall()
            for i, (name, dni) in enumerate(registros, start=1):
                row_frame = ttk.Frame(table_frame, style="Table.TFrame")
                row_frame.pack(fill="x")
                
                name_label = ttk.Label(row_frame, text=name, style="Table.TLabel")
                name_label.grid(row=i, column=0, padx=10, pady=5)

                dni_label = ttk.Label(row_frame, text=dni, style="Table.TLabel")
                dni_label.grid(row=i, column=1, padx=10, pady=5)
            conexion.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error al leer la base de datos: {e}")

    def buscar_alumno(self) -> None:
        ventana_buscar = tk.Toplevel(self.root)
        ventana_buscar.geometry("500x400")
        ventana_buscar.title("Perfil del Estudiante")
        ventana_buscar.configure(bg=COLOR_FONDO)

        ttk.Label(ventana_buscar, text="Ingresa el número de DNI a buscar:", font=("Helvetica", 12)).pack(pady=(20, 10))

        buscar_dni_ = tk.StringVar()
        ttk.Entry(ventana_buscar, width=40, textvariable=buscar_dni_).pack(pady=5)

        resultado_label = ttk.Label(ventana_buscar, text="", font=("Helvetica", 12))
        resultado_label.pack(pady=10)

        def accion_buscar() -> None:
            dni = buscar_dni_.get()
            if not dni:
                messagebox.showerror("Error", "Por favor, ingresa el número de DNI.")
                return

            try:
                conexion = sqlite3.connect(BASE_DATOS)
                cursor = conexion.cursor()
                cursor.execute("SELECT * FROM alumnos WHERE dni = ?", (dni,))
                alumno = cursor.fetchone()
                conexion.close()
                if alumno:
                    self.mostrar_resultado_busqueda(ventana_buscar, alumno)
                else:
                    messagebox.showinfo("Resultado", "No se encontró ningún alumno con ese DNI.")
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error: {e}")

        ttk.Button(ventana_buscar, text="Buscar", command=accion_buscar).pack(pady=10)
        ttk.Button(ventana_buscar, text="Cerrar", command=ventana_buscar.destroy).pack(pady=10)

    def mostrar_resultado_busqueda(self, ventana, alumno):
        for widget in ventana.winfo_children():
            widget.destroy()

        resultado_label = tk.Label(ventana, text="Perfil del Estudiante", font=("Arial", 20, "bold"), bg=COLOR_FONDO)
        resultado_label.pack(pady=20)

        card_frame = ttk.Frame(ventana, padding="10", style="Card.TFrame")
        card_frame.pack(fill="both", expand=True, padx=20, pady=10)

        header_frame = ttk.Frame(card_frame, style="Card.TFrame")
        header_frame.pack(fill="x")

        header_title = tk.Label(header_frame, text=f"{alumno[1]} {alumno[2]}", font=("Arial", 16, "bold"), bg=COLOR_FONDO)
        header_title.pack(anchor="w")

        header_description = tk.Label(header_frame, text=f"Estudiante de {alumno[3]}", font=("Arial", 12), bg=COLOR_FONDO)
        header_description.pack(anchor="w")

        content_frame = ttk.Frame(card_frame, style="Card.TFrame")
        content_frame.pack(fill="both", expand=True)

        details = [
            ("Número de Identificación:", alumno[0]),
            ("Fecha de Nacimiento:", alumno[4]),
            ("Dirección:", alumno[6]),
            ("Teléfono:", alumno[7])
        ]

        for label, value in details:
            row_frame = ttk.Frame(content_frame, padding="5", style="Card.TFrame")
            row_frame.pack(fill="x", padx=10, pady=5)

            label_widget = tk.Label(row_frame, text=label, font=("Arial", 12), bg=COLOR_FONDO)
            label_widget.pack(side="left")

            value_widget = tk.Label(row_frame, text=value, font=("Arial", 12, "bold"), bg=COLOR_FONDO)
            value_widget.pack(side="left", padx=10)

    def eliminar_alumno(self) -> None:
        ventana_eliminar = tk.Toplevel(self.root)
        ventana_eliminar.geometry("400x300")
        ventana_eliminar.title("Sección para eliminar alumno")
        ventana_eliminar.configure(bg=COLOR_FONDO)

        ttk.Label(ventana_eliminar, text="Ingresa el número de DNI del alumno a eliminar:", font=("Helvetica", 12)).pack(pady=(20, 10))

        eliminar_dni_ = tk.StringVar()
        ttk.Entry(ventana_eliminar, width=40, textvariable=eliminar_dni_).pack(pady=5)

        def accion_eliminar() -> None:
            dni = eliminar_dni_.get()
            if not dni:
                messagebox.showerror("Error", "Por favor, ingresa el número de DNI.")
                return

            try:
                conexion = sqlite3.connect(BASE_DATOS)
                cursor = conexion.cursor()
                cursor.execute("DELETE FROM alumnos WHERE dni = ?", (dni,))
                conexion.commit()
                conexion.close()
                if cursor.rowcount > 0:
                    messagebox.showinfo("Eliminación exitosa", "El alumno ha sido eliminado correctamente.")
                else:
                    messagebox.showinfo("Eliminación fallida", "No se encontró ningún alumno con ese DNI.")
                ventana_eliminar.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error: {e}")

        ttk.Button(ventana_eliminar, text="Eliminar", command=accion_eliminar).pack(pady=10)
        ttk.Button(ventana_eliminar, text="Cerrar", command=ventana_eliminar.destroy).pack(pady=10)

    def mostrar_mensaje(self, mensaje):
        messagebox.showinfo("Mensaje", mensaje)

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaMatriculas(root)
    root.mainloop()
