import tkinter as tk  # Importa la librería tkinter para crear la interfaz gráfica
from tkinter import messagebox, scrolledtext  # Importa clases específicas de tkinter
import csv  # Importa el módulo csv para trabajar con archivos CSV

# Constantes
ARCHIVO_CSV = "base_matricula.csv"  # Nombre del archivo CSV donde se almacenarán los datos

# Funciones

def guardar_datos(datos: list) -> bool:
    """Guarda los datos en un archivo CSV."""
    try:
        with open(ARCHIVO_CSV, 'a', newline='') as csvfile:  # Abre el archivo CSV en modo 'a' (append)
            csvwriter = csv.writer(csvfile)  # Crea un objeto csv.writer
            csvwriter.writerow(datos)  # Escribe una fila de datos en el archivo CSV
        return True  # Retorna True si se guardaron los datos correctamente
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar los datos: {e}")  # Muestra un mensaje de error
        return False  # Retorna False si hubo un error al guardar los datos

def validar_dni(dni: str) -> bool:
    """Valida que el DNI tenga exactamente 8 caracteres numéricos."""
    return len(dni) == 8 and dni.isdigit()  # Retorna True si el DNI tiene 8 dígitos numéricos

def validar_campos(campos: list) -> bool:
    """Valida que todos los campos estén llenos y que el DNI sea válido."""
    for campo in campos:
        if not campo:  # Verifica si algún campo está vacío
            return False  # Retorna False si algún campo está vacío
    return validar_dni(campos[1])  # Retorna el resultado de validar el DNI

def accion_matricula(nombre_var, dni_var, fecha_nacimiento_var, nombre_padre_var, direccion_var, telefono_padre_var, ventana_matricula):
    """Acción para registrar una nueva matrícula."""
    datos = [
        nombre_var.get(), dni_var.get(), fecha_nacimiento_var.get(),
        nombre_padre_var.get(), direccion_var.get(), telefono_padre_var.get()
    ]  # Obtiene los datos de las variables de entrada

    if not validar_campos(datos):  # Verifica si los campos son válidos
        messagebox.showerror("Error", "Todos los campos son obligatorios y el DNI debe tener 8 dígitos.")  # Muestra un mensaje de error
        return  # Retorna si hay algún error en los campos

    if guardar_datos(datos):  # Intenta guardar los datos
        messagebox.showinfo("Matriculación Exitosa", "El alumno se ha matriculado correctamente.")  # Muestra un mensaje de éxito
        ventana_matricula.destroy()  # Cierra la ventana de matrícula después de matricular al alumno

def crear_entrada(ventana, texto, variable):
    """Crea una etiqueta y una entrada de texto en la ventana especificada."""
    frame = tk.Frame(ventana)  # Crea un frame en la ventana especificada
    frame.pack(pady=5)  # Empaqueta el frame con un padding vertical de 5

    label = tk.Label(frame, text=texto, width=20, anchor="w", bg="#F0E68C")  # Crea una etiqueta con texto, ancho y color de fondo
    label.pack(side=tk.LEFT)  # Empaqueta la etiqueta a la izquierda del frame

    entry = tk.Entry(frame, width=40, textvariable=variable)  # Crea una entrada de texto con ancho y variable asociada
    entry.pack(side=tk.LEFT)  # Empaqueta la entrada de texto a la izquierda del frame

    return entry  # Retorna la entrada de texto creada

def matricula():
    """Crea la ventana para matricular un nuevo alumno."""
    ventana_matricula = tk.Toplevel(root)  # Crea una nueva ventana secundaria
    ventana_matricula.geometry("600x400")  # Establece las dimensiones de la ventana
    ventana_matricula.title("Matrícula de Alumnos")  # Establece el título de la ventana
    ventana_matricula.configure(bg="#F0E68C")  # Establece el color de fondo de la ventana

    # Variables para almacenar los datos del alumno
    nombre_var = tk.StringVar()
    dni_var = tk.StringVar()
    fecha_nacimiento_var = tk.StringVar()
    nombre_padre_var = tk.StringVar()
    direccion_var = tk.StringVar()
    telefono_padre_var = tk.StringVar()

    # Crea las entradas para cada campo
    crear_entrada(ventana_matricula, "Nombre del alumno:", nombre_var)
    crear_entrada(ventana_matricula, "DNI del alumno:", dni_var)
    crear_entrada(ventana_matricula, "Fecha de nacimiento:", fecha_nacimiento_var)
    crear_entrada(ventana_matricula, "Nombre del padre:", nombre_padre_var)
    crear_entrada(ventana_matricula, "Dirección:", direccion_var)
    crear_entrada(ventana_matricula, "Teléfono del padre:", telefono_padre_var)

    # Botón para registrar la matrícula
    button_registrar = tk.Button(
        ventana_matricula, text="Registrar alumno",
        command=lambda: accion_matricula(
            nombre_var, dni_var, fecha_nacimiento_var, nombre_padre_var,
            direccion_var, telefono_padre_var, ventana_matricula
        )
    )
    button_registrar.pack(pady=10)  # Empaqueta el botón con un padding vertical de 10

def mostrar_alumnos():
    """Crea la ventana para mostrar la base de alumnos matriculados."""
    ventana_base = tk.Toplevel(root)  # Crea una nueva ventana secundaria
    ventana_base.geometry("800x600")  # Establece las dimensiones de la ventana
    ventana_base.title("Base de Alumnos")  # Establece el título de la ventana
    ventana_base.configure(bg="#F0E68C")  # Establece el color de fondo de la ventana

    label = tk.Label(ventana_base, text="Alumnos Matriculados", bg="#F0E68C", font=("Helvetica", 16, "bold"))  # Crea una etiqueta con texto, color de fondo y fuente
    label.pack(pady=(20, 10))  # Empaqueta la etiqueta con un padding vertical de 20 a 10

    texto_desplazado = scrolledtext.ScrolledText(ventana_base, width=100, height=20)  # Crea un área de texto desplazable con ancho y alto
    texto_desplazado.pack(expand=True, fill="both", padx=20)  # Empaqueta el área de texto, expandiéndolo y llenando el espacio

    try:
        with open(ARCHIVO_CSV, newline="") as archivo:  # Abre el archivo CSV
            lector_csv = csv.reader(archivo)  # Crea un lector CSV
            for fila in lector_csv:
                texto_desplazado.insert(tk.END, ", ".join(fila) + "\n")  # Inserta cada fila del archivo CSV en el área de texto
    except FileNotFoundError:
        texto_desplazado.insert(tk.END, "El archivo CSV no se encontró.")  # Muestra un mensaje si no se encuentra el archivo CSV
    except Exception as e:
        texto_desplazado.insert(tk.END, f"Error al leer el archivo: {e}")  # Muestra un mensaje si ocurre un error al leer el archivo

def buscar_alumno():
    """Crea la ventana para buscar un alumno por DNI."""
    ventana_buscar = tk.Toplevel(root)  # Crea una nueva ventana secundaria
    ventana_buscar.geometry("400x200")  # Establece las dimensiones de la ventana
    ventana_buscar.title("Buscar Alumno")  # Establece el título de la ventana
    ventana_buscar.configure(bg="#F0E68C")  # Establece el color de fondo de la ventana

    label = tk.Label(ventana_buscar, text="Buscar Alumno por DNI", bg="#F0E68C", font=("Helvetica", 12))  # Crea una etiqueta con texto, color de fondo y fuente
    label.pack(pady=(20, 10))  # Empaqueta la etiqueta con un padding vertical de 20 a 10

    buscar_dni_ = tk.StringVar()  # Crea una variable de cadena para almacenar el DNI a buscar
    buscar_dni_entry = tk.Entry(ventana_buscar, width=30, textvariable=buscar_dni_)  # Crea una entrada de texto con ancho y variable asociada
    buscar_dni_entry.pack()  # Empaqueta la entrada de texto

    resultado_label = tk.Label(ventana_buscar, text="", font=("Helvetica", 12))  # Crea una etiqueta para mostrar el resultado, con fuente
    resultado_label.pack(pady=10)  # Empaqueta la etiqueta con un padding vertical de 10

    def accion_buscar():
        """Acción para buscar un alumno en la base de datos."""
        dni = buscar_dni_.get()  # Obtiene el DNI a buscar desde la variable
        if not dni:  # Verifica si no se ha ingresado ningún DNI
            messagebox.showerror("Error", "Por favor, ingresa el número de DNI.")  # Muestra un mensaje de error si no se ha ingresado un DNI
            return  # Retorna si no se ha ingresado un DNI válido

        try:
            encontrado = False  # Bandera para indicar si se encontró el alumno
            with open(ARCHIVO_CSV, newline="") as archivo:  # Abre el archivo CSV en modo lectura
                lector_csv = csv.reader(archivo)  # Crea un lector CSV
                for fila in lector_csv:
                    if dni == fila[1]:  # Compara el DNI buscado con el DNI en la fila actual
                        encontrado = True  # Marca como encontrado
                        resultado_label.config(text="Resultado encontrado:\n" + ", ".join(fila))  # Muestra el resultado encontrado
                        break  # Sale del bucle una vez encontrado el alumno
                if not encontrado:  # Si no se encontró el alumno
                    messagebox.showinfo("Resultado", "No se encontró ningún alumno con ese DNI.")  # Muestra un mensaje informativo
        except FileNotFoundError:  # Manejo de excepción si no se encuentra el archivo CSV
            messagebox.showerror("Error", "El archivo CSV no se encontró.")  # Muestra un mensaje de error
        except Exception as e:  # Manejo de excepción genérico
            messagebox.showerror("Error", f"Ocurrió un error: {e}")  # Muestra un mensaje de error con el detalle

    buscar_button = tk.Button(ventana_buscar, text="Buscar", command=accion_buscar)  # Crea un botón para buscar un alumno
    buscar_button.pack(pady=10)  # Empaqueta el botón con un padding vertical de 10

def eliminar_alumno():
    """Crea la ventana para eliminar un alumno por DNI."""
    ventana_eliminar = tk.Toplevel(root)  # Crea una nueva ventana secundaria
    ventana_eliminar.geometry("400x200")  # Establece las dimensiones de la ventana
    ventana_eliminar.title("Eliminar Alumno")  # Establece el título de la ventana
    ventana_eliminar.configure(bg="#F0E68C")  # Establece el color de fondo de la ventana

    label = tk.Label(ventana_eliminar, text="Eliminar Alumno por DNI", bg="#F0E68C", font=("Helvetica", 12))  # Crea una etiqueta con texto, color de fondo y fuente
    label.pack(pady=(20, 10))  # Empaqueta la etiqueta con un padding vertical de 20 a 10

    eliminar_dni_ = tk.StringVar()  # Crea una variable de cadena para almacenar el DNI a eliminar
    eliminar_dni_entry = tk.Entry(ventana_eliminar, width=30, textvariable=eliminar_dni_)  # Crea una entrada de texto con ancho y variable asociada
    eliminar_dni_entry.pack()  # Empaqueta la entrada de texto

    def accion_eliminar():
        """Acción para eliminar un alumno de la base de datos."""
        dni = eliminar_dni_.get()  # Obtiene el DNI a eliminar desde la variable
        if not dni:  # Verifica si no se ha ingresado ningún DNI
            messagebox.showerror("Error", "Por favor, ingresa el número de DNI.")  # Muestra un mensaje de error si no se ha ingresado un DNI
            return  # Retorna si no se ha ingresado un DNI válido

        try:
            with open(ARCHIVO_CSV, "r") as archivo:  # Abre el archivo CSV en modo lectura
                lineas = archivo.readlines()  # Lee todas las líneas del archivo CSV

            with open(ARCHIVO_CSV, "w", newline='') as archivo:  # Abre el archivo CSV en modo escritura
                csvwriter = csv.writer(archivo)  # Crea un escritor CSV
                eliminado = False  # Bandera para indicar si se eliminó el alumno
                for linea in lineas:
                    fila = linea.strip().split(',')  # Divide la línea en una lista de columnas
                    if dni != fila[1]:  # Compara el DNI a eliminar con el DNI en la fila actual
                        csvwriter.writerow(fila)  # Escribe la fila en el archivo CSV
                    else:
                        eliminado = True  # Marca como eliminado
                if eliminado:
                    messagebox.showinfo("Eliminación exitosa", "El alumno ha sido eliminado correctamente.")  # Muestra un mensaje de eliminación exitosa
                else:
                    messagebox.showinfo("Eliminación fallida", "No se encontró ningún alumno con ese DNI.")  # Muestra un mensaje de eliminación fallida
                ventana_eliminar.destroy()  # Cierra la ventana de eliminación
        except FileNotFoundError:  # Manejo de excepción si no se encuentra el archivo CSV
            messagebox.showerror("Error", "El archivo CSV no se encontró.")  # Muestra un mensaje de error
        except Exception as e:  # Manejo de excepción genérico
            messagebox.showerror("Error", f"Ocurrió un error: {e}")  # Muestra un mensaje de error con el detalle

    eliminar_button = tk.Button(ventana_eliminar, text="Eliminar", command=accion_eliminar)  # Crea un botón para eliminar un alumno
    eliminar_button.pack(pady=10)  # Empaqueta el botón con un padding vertical de 10

# Configuración de la ventana principal
root = tk.Tk()  # Crea la ventana principal
root.geometry("800x600")  # Establece las dimensiones de la ventana principal
root.title("Sistema de Matrículas Escolares")  # Establece el título de la ventana principal
root.configure(bg="#F0E68C")  # Establece el color de fondo de la ventana principal

# Etiqueta principal
label = tk.Label(root, text="Institución Educativa Pública General Emilio Soyer Cabero", font=("Helvetica", 20, "bold"), bg="#F0E68C")  # Crea una etiqueta con texto, fuente y color de fondo
label.pack(pady=30)  # Empaqueta la etiqueta con un padding vertical de 30

# Frame para los botones
seccion_botones = tk.Frame(root, bg="#F0E68C")  # Crea un frame con color de fondo
seccion_botones.pack(pady=20)  # Empaqueta el frame con un padding vertical de 20

# Botones principales
button1 = tk.Button(seccion_botones, text="Matricular Alumno", command=matricula, width=20, height=2)  # Crea un botón para matricular un alumno
button1.pack(side=tk.LEFT, padx=10)  # Empaqueta el botón a la izquierda con un padding horizontal de 10

button2 = tk.Button(seccion_botones, text="Ver Base de Alumnos", command=mostrar_alumnos, width=20, height=2)  # Crea un botón para mostrar la base de alumnos
button2.pack(side=tk.LEFT, padx=10)  # Empaqueta el botón a la izquierda con un padding horizontal de 10

button3 = tk.Button(seccion_botones, text="Buscar Alumno", command=buscar_alumno, width=20, height=2)  # Crea un botón para buscar un alumno
button3.pack(side=tk.LEFT, padx=10)  # Empaqueta el botón a la izquierda con un padding horizontal de 10

button4 = tk.Button(seccion_botones, text="Eliminar Alumno", command=eliminar_alumno, width=20, height=2)  # Crea un botón para eliminar un alumno
button4.pack(side=tk.LEFT, padx=10)  # Empaqueta el botón a la izquierda con un padding horizontal de 10

root.mainloop()  # Ejecuta el loop principal de la ventana

