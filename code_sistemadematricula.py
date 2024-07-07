import tkinter as tk  # Importa el módulo tkinter para crear interfaces gráficas
from tkinter import ttk, messagebox, scrolledtext  # Importa componentes adicionales de tkinter
import sqlite3  # Importa el módulo sqlite3 para manejar la base de datos SQLite
import uuid  # Importa el módulo uuid para generar identificadores únicos
from datetime import datetime  # Importa datetime para manejar fechas y horas
from typing import List  # Importa List de typing para las anotaciones de tipo

# Constantes
BASE_DATOS = "base_matricula.db"  # Nombre del archivo de la base de datos SQLite
COLOR_FONDO = "#F0E68C"  # Color de fondo de la interfaz

class SistemaMatriculas:
    def __init__(self, root: tk.Tk):
        # Configuración inicial de la ventana principal
        self.root = root  # Almacena la ventana principal
        self.root.geometry("800x600")  # Establece el tamaño de la ventana
        self.root.title("Sistema de Matrículas Escolares")  # Establece el título de la ventana
        self.root.configure(bg=COLOR_FONDO)  # Establece el color de fondo de la ventana

        # Configuración del estilo para widgets ttk
        self.style = ttk.Style()  # Crea un objeto de estilo
        self.style.theme_use('clam')  # Usa un tema ttk predefinido
        self.style.configure("TFrame", background=COLOR_FONDO)  # Configura el estilo del frame
        self.style.configure("TLabel", background=COLOR_FONDO, font=("Helvetica", 12))  # Configura el estilo de las etiquetas
        self.style.configure("TButton", background=COLOR_FONDO, font=("Helvetica", 12, "bold"), padding=6)  # Configura el estilo de los botones
        self.style.configure("TEntry", padding=6, font=("Helvetica", 12))  # Configura el estilo de las entradas

        # Etiqueta principal con el nombre de la institución
        self.label = tk.Label(root, text="I.E. Miguel Grau y Seminario", font=("Helvetica", 20, "bold"), bg=COLOR_FONDO)  # Crea la etiqueta principal
        self.label.pack(pady=30)  # Empaqueta la etiqueta en la ventana principal con un margen vertical

        # Frame para los botones principales
        self.seccion_botones = ttk.Frame(root)  # Crea un frame para los botones
        self.seccion_botones.pack(pady=20)  # Empaqueta el frame en la ventana principal con un margen vertical

        # Botones principales para las diferentes acciones
        self.button1 = ttk.Button(self.seccion_botones, text="Matricular Alumno", command=self.matricula, width=20)  # Crea el botón para matricular un alumno
        self.button1.pack(side=tk.LEFT, padx=10)  # Empaqueta el botón en el frame con un margen horizontal

        self.button2 = ttk.Button(self.seccion_botones, text="Ver Base de Alumnos", command=self.mostrar_alumnos, width=20)  # Crea el botón para ver la base de alumnos
        self.button2.pack(side=tk.LEFT, padx=10)  # Empaqueta el botón en el frame con un margen horizontal

        self.button3 = ttk.Button(self.seccion_botones, text="Buscar Alumno", command=self.buscar_alumno, width=20)  # Crea el botón para buscar un alumno
        self.button3.pack(side=tk.LEFT, padx=10)  # Empaqueta el botón en el frame con un margen horizontal

        self.button4 = ttk.Button(self.seccion_botones, text="Eliminar Alumno", command=self.eliminar_alumno, width=20)  # Crea el botón para eliminar un alumno
        self.button4.pack(side=tk.LEFT, padx=10)  # Empaqueta el botón en el frame con un margen horizontal

        # Inicializar la base de datos
        self.inicializar_base_datos()

    def inicializar_base_datos(self):
        """Inicializa la base de datos y crea la tabla de alumnos si no existe."""
        conexion = sqlite3.connect(BASE_DATOS)  # Conecta con la base de datos
        cursor = conexion.cursor()  # Crea un cursor para interactuar con la base de datos
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
        ''')  # Crea la tabla de alumnos si no existe
        conexion.commit()  # Guarda los cambios
        conexion.close()  # Cierra la conexión

    def guardar_datos(self, datos: List[str]) -> bool:
        """Guarda los datos en la base de datos SQLite."""
        try:
            conexion = sqlite3.connect(BASE_DATOS)  # Conecta con la base de datos
            cursor = conexion.cursor()  # Crea un cursor para interactuar con la base de datos
            cursor.execute('''
                INSERT INTO alumnos (id, nombre, apellido, dni, fecha_nacimiento, nombre_padre, direccion, telefono_padre, hora_matricula)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', datos)  # Inserta los datos en la tabla de alumnos
            conexion.commit()  # Guarda los cambios
            conexion.close()  # Cierra la conexión
            return True  # Retorna True si se guarda correctamente
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "El DNI ya está registrado.")  # Muestra un mensaje de error si el DNI ya está registrado
            return False  # Retorna False si ocurre un error
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar los datos: {e}")  # Muestra un mensaje de error si ocurre una excepción
            return False  # Retorna False si ocurre un error

    def validar_dni(self, dni: str) -> bool:
        """Valida que el DNI tenga exactamente 8 caracteres numéricos."""
        return len(dni) == 8 and dni.isdigit()  # Retorna True si el DNI tiene 8 dígitos numéricos

    def validar_campos(self, campos: List[str]) -> bool:
        """Valida que todos los campos estén llenos y que el DNI sea válido."""
        for campo in campos:
            if not campo:  # Si algún campo está vacío
                return False  # Retorna False
        return self.validar_dni(campos[2])  # Valida el campo DNI y retorna el resultado

    def accion_matricula(self, nombre_var, apellido_var, dni_var, fecha_nacimiento_var, nombre_padre_var, direccion_var, telefono_padre_var, detalles_frame):
        """Acción para registrar una nueva matrícula."""
        id_unico = str(uuid.uuid4())  # Genera un ID único
        hora_matricula = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Obtiene la fecha y hora actual
        datos = [
            id_unico, nombre_var.get(), apellido_var.get(), dni_var.get(), fecha_nacimiento_var.get(),
            nombre_padre_var.get(), direccion_var.get(), telefono_padre_var.get(), hora_matricula
        ]  # Crea una lista con los datos de la matrícula

        if not self.validar_campos(datos[1:8]):  # Valida solo los campos de nombre a teléfono
            messagebox.showerror("Error", "Todos los campos son obligatorios y el DNI debe tener 8 dígitos.")  # Muestra un mensaje de error si la validación falla
            return

        if self.guardar_datos(datos):  # Si los datos se guardan correctamente
            messagebox.showinfo("Matriculación Exitosa", "El alumno se ha matriculado correctamente.")  # Muestra un mensaje de éxito
            self.mostrar_detalles_matricula(detalles_frame, id_unico, apellido_var.get(), hora_matricula)  # Muestra los detalles de la matrícula
            self.limpiar_campos([nombre_var, apellido_var, dni_var, fecha_nacimiento_var, nombre_padre_var, direccion_var, telefono_padre_var])  # Limpia los campos del formulario

    def crear_entrada(self, ventana: ttk.Frame, texto: str, variable: tk.StringVar, fila: int, columna: int) -> ttk.Entry:
        """Crea una etiqueta y una entrada de texto en la ventana especificada."""
        label = ttk.Label(ventana, text=texto)  # Crea una etiqueta con el texto especificado
        label.grid(row=fila, column=columna, padx=10, pady=5, sticky="E")  # Coloca la etiqueta en la cuadrícula
        entry = ttk.Entry(ventana, width=40, textvariable=variable)  # Crea una entrada de texto asociada a la variable especificada
        entry.grid(row=fila, column=columna+1, padx=10, pady=5)  # Coloca la entrada en la cuadrícula
        return entry  # Retorna la entrada creada

    def limpiar_campos(self, campos: List[tk.StringVar]) -> None:
        """Limpia el contenido de los campos especificados."""
        for campo in campos:
            campo.set("")  # Establece el valor de cada campo en una cadena vacía

    def mostrar_detalles_matricula(self, frame, id_unico: str, apellido: str, hora_matricula: str) -> None:
        """Muestra los detalles de la matrícula en el frame especificado."""
        for widget in frame.winfo_children():
            widget.destroy()  # Elimina todos los widgets hijos del frame
        
        ttk.Label(frame, text=f"ID: {id_unico}", font=("Helvetica", 12)).pack(pady=5)  # Muestra el ID de la matrícula
        ttk.Label(frame, text=f"Apellido: {apellido}", font=("Helvetica", 12)).pack(pady=5)  # Muestra el apellido del alumno
        ttk.Label(frame, text=f"Hora de Matrícula: {hora_matricula}", font=("Helvetica", 12)).pack(pady=5)  # Muestra la hora de matrícula

    def matricula(self) -> None:
        """Crea la ventana para matricular un nuevo alumno."""
        ventana_matricula = tk.Toplevel()  # Crea una nueva ventana
        ventana_matricula.geometry("600x700")  # Establece el tamaño de la ventana
        ventana_matricula.title("Sección de Matrícula")  # Establece el título de la ventana
        ventana_matricula.configure(bg=COLOR_FONDO)  # Establece el color de fondo de la ventana

        # Variables para los campos de entrada
        nombre_var = tk.StringVar()  # Variable para el nombre del alumno
        apellido_var = tk.StringVar()  # Variable para el apellido del alumno
        dni_var = tk.StringVar()  # Variable para el DNI del alumno
        fecha_nacimiento_var = tk.StringVar()  # Variable para la fecha de nacimiento del alumno
        nombre_padre_var = tk.StringVar()  # Variable para el nombre del padre o apoderado
        direccion_var = tk.StringVar()  # Variable para la dirección
        telefono_padre_var = tk.StringVar()  # Variable para el teléfono del apoderado

        # Etiqueta informativa en la ventana de matrícula
        ttk.Label(ventana_matricula, text="Estás en la sección de matrículas", font=("Helvetica", 16, "bold")).pack(pady=(20, 10))

        # Frame para el formulario de matrícula
        formulario = ttk.Frame(ventana_matricula)  # Crea un frame para el formulario
        formulario.pack(pady=20)  # Empaqueta el frame con un margen vertical

        # Crear entradas de texto en el formulario usando la cuadrícula
        self.crear_entrada(formulario, "Nombre del alumno:", nombre_var, 0, 0)  # Entrada para el nombre del alumno
        self.crear_entrada(formulario, "Apellido del alumno:", apellido_var, 1, 0)  # Entrada para el apellido del alumno
        self.crear_entrada(formulario, "DNI del alumno:", dni_var, 2, 0)  # Entrada para el DNI del alumno
        self.crear_entrada(formulario, "Fecha de nacimiento:", fecha_nacimiento_var, 3, 0)  # Entrada para la fecha de nacimiento del alumno
        self.crear_entrada(formulario, "Nombre del padre o apoderado:", nombre_padre_var, 4, 0)  # Entrada para el nombre del padre o apoderado
        self.crear_entrada(formulario, "Dirección:", direccion_var, 5, 0)  # Entrada para la dirección
        self.crear_entrada(formulario, "Teléfono del apoderado:", telefono_padre_var, 6, 0)  # Entrada para el teléfono del apoderado

        # Frame para mostrar detalles de la matrícula
        detalles_frame = ttk.Frame(ventana_matricula)  # Crea un frame para los detalles
        detalles_frame.pack(pady=20)  # Empaqueta el frame con un margen vertical

        # Botón para registrar al alumno
        ttk.Button(
            ventana_matricula, text="Registrar alumno",
            command=lambda: self.accion_matricula(
                nombre_var, apellido_var, dni_var, fecha_nacimiento_var, nombre_padre_var,
                direccion_var, telefono_padre_var, detalles_frame)
        ).pack(pady=20)  # Empaqueta el botón con un margen vertical

    def mostrar_alumnos(self) -> None:
        """Crea la ventana para mostrar la base de alumnos matriculados."""
        ventana_base = tk.Toplevel(self.root)  # Crea una nueva ventana
        ventana_base.geometry("600x500")  # Establece el tamaño de la ventana
        ventana_base.title("Sección base de alumnos")  # Establece el título de la ventana
        ventana_base.configure(bg=COLOR_FONDO)  # Establece el color de fondo de la ventana

        # Etiqueta informativa en la ventana de base de alumnos
        ttk.Label(ventana_base, text="Alumnos Matriculados:", font=("Helvetica", 16, "bold")).pack(pady=(20, 10))

        # Texto desplazable para mostrar la base de alumnos
        texto_desplazado = scrolledtext.ScrolledText(ventana_base, width=70, height=20, font=("Helvetica", 12))  # Crea un área de texto desplazable
        texto_desplazado.pack(expand=True, fill="both", padx=20, pady=10)  # Empaqueta el área de texto con expansión y margen

        # Intenta leer y mostrar los datos de la base de datos
        try:
            conexion = sqlite3.connect(BASE_DATOS)  # Conecta con la base de datos
            cursor = conexion.cursor()  # Crea un cursor para interactuar con la base de datos
            cursor.execute("SELECT * FROM alumnos")  # Selecciona todos los registros de la tabla de alumnos
            registros = cursor.fetchall()  # Obtiene todos los registros
            for fila in registros:
                texto_desplazado.insert(tk.END, ", ".join(fila) + "\n")  # Inserta cada fila en el área de texto
            conexion.close()  # Cierra la conexión
        except Exception as e:
            texto_desplazado.insert(tk.END, f"Error al leer la base de datos: {e}")  # Muestra un mensaje de error si ocurre una excepción

    def buscar_alumno(self) -> None:
        """Crea la ventana para buscar un alumno por DNI."""
        ventana_buscar = tk.Toplevel(self.root)  # Crea una nueva ventana
        ventana_buscar.geometry("700x400")  # Establece el tamaño de la ventana
        ventana_buscar.title("Sección para buscar alumno")  # Establece el título de la ventana
        ventana_buscar.configure(bg=COLOR_FONDO)  # Establece el color de fondo de la ventana

        # Etiqueta informativa en la ventana de búsqueda
        ttk.Label(ventana_buscar, text="Ingresa el número de DNI a buscar:", font=("Helvetica", 12)).pack(pady=(20, 10))

        buscar_dni_ = tk.StringVar()  # Variable para el DNI a buscar
        ttk.Entry(ventana_buscar, width=40, textvariable=buscar_dni_).pack(pady=5)  # Entrada de texto para el DNI

        resultado_label = ttk.Label(ventana_buscar, text="", font=("Helvetica", 12))  # Etiqueta para mostrar el resultado
        resultado_label.pack(pady=10)  # Empaqueta la etiqueta con un margen vertical

        # Acción para buscar un alumno en la base de datos
        def accion_buscar() -> None:
            dni = buscar_dni_.get()  # Obtiene el DNI ingresado
            if not dni:  # Si no se ingresó un DNI
                messagebox.showerror("Error", "Por favor, ingresa el número de DNI.")  # Muestra un mensaje de error
                return

            # Intenta buscar el alumno en la base de datos
            try:
                conexion = sqlite3.connect(BASE_DATOS)  # Conecta con la base de datos
                cursor = conexion.cursor()  # Crea un cursor para interactuar con la base de datos
                cursor.execute("SELECT * FROM alumnos WHERE dni = ?", (dni,))  # Busca el alumno por DNI
                alumno = cursor.fetchone()  # Obtiene el primer resultado
                conexion.close()  # Cierra la conexión
                if alumno:
                    resultado_label.config(text="Resultado encontrado:\n" + ", ".join(alumno))  # Muestra los datos del alumno
                else:
                    messagebox.showinfo("Resultado", "No se encontró ningún alumno con ese DNI.")  # Muestra un mensaje si no se encuentra el alumno
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error: {e}")  # Muestra un mensaje de error si ocurre una excepción

        ttk.Button(ventana_buscar, text="Buscar", command=accion_buscar).pack(pady=10)  # Botón para iniciar la búsqueda
        ttk.Button(ventana_buscar, text="Cerrar", command=ventana_buscar.destroy).pack(pady=10)  # Botón para cerrar la ventana

    def eliminar_alumno(self) -> None:
        """Crea la ventana para eliminar un alumno por DNI."""
        ventana_eliminar = tk.Toplevel(self.root)  # Crea una nueva ventana
        ventana_eliminar.geometry("400x300")  # Establece el tamaño de la ventana
        ventana_eliminar.title("Sección para eliminar alumno")  # Establece el título de la ventana
        ventana_eliminar.configure(bg=COLOR_FONDO)  # Establece el color de fondo de la ventana

        # Etiqueta informativa en la ventana de eliminación
        ttk.Label(ventana_eliminar, text="Ingresa el número de DNI del alumno a eliminar:", font=("Helvetica", 12)).pack(pady=(20, 10))

        eliminar_dni_ = tk.StringVar()  # Variable para el DNI a eliminar
        ttk.Entry(ventana_eliminar, width=40, textvariable=eliminar_dni_).pack(pady=5)  # Entrada de texto para el DNI

        # Acción para eliminar un alumno de la base de datos
        def accion_eliminar() -> None:
            dni = eliminar_dni_.get()  # Obtiene el DNI ingresado
            if not dni:  # Si no se ingresó un DNI
                messagebox.showerror("Error", "Por favor, ingresa el número de DNI.")  # Muestra un mensaje de error
                return

            # Intenta eliminar el alumno de la base de datos
            try:
                conexion = sqlite3.connect(BASE_DATOS)  # Conecta con la base de datos
                cursor = conexion.cursor()  # Crea un cursor para interactuar con la base de datos
                cursor.execute("DELETE FROM alumnos WHERE dni = ?", (dni,))  # Elimina el alumno por DNI
                conexion.commit()  # Guarda los cambios
                conexion.close()  # Cierra la conexión
                if cursor.rowcount > 0:
                    messagebox.showinfo("Eliminación exitosa", "El alumno ha sido eliminado correctamente.")  # Muestra un mensaje de éxito
                else:
                    messagebox.showinfo("Eliminación fallida", "No se encontró ningún alumno con ese DNI.")  # Muestra un mensaje si no se encuentra el alumno
                ventana_eliminar.destroy()  # Cierra la ventana de eliminación
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error: {e}")  # Muestra un mensaje de error si ocurre una excepción

        ttk.Button(ventana_eliminar, text="Eliminar", command=accion_eliminar).pack(pady=10)  # Botón para iniciar la eliminación
        ttk.Button(ventana_eliminar, text="Cerrar", command=ventana_eliminar.destroy).pack(pady=10)  # Botón para cerrar la ventana

if __name__ == "__main__":
    root = tk.Tk()  # Crea la ventana principal
    app = SistemaMatriculas(root)  # Crea una instancia de la clase SistemaMatriculas
    root.mainloop()  # Inicia el bucle principal de la ventana
