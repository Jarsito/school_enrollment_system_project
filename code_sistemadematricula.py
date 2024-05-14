import tkinter as tk
import csv
import tkinter.messagebox as messagebox 
from tkinter import scrolledtext

def accion_matricula(nombre_var, dni_var, fecha_nacimiento_var, nombre_padre_var, direccion_var, telefono_padre_var, ventana_matricula):
    nombre = nombre_var.get()
    dni = dni_var.get()
    fecha_nacimiento = fecha_nacimiento_var.get()
    nombre_padre = nombre_padre_var.get()
    direccion = direccion_var.get()
    telefono_padre = telefono_padre_var.get()
    
    datos = [nombre, dni, fecha_nacimiento, nombre_padre, direccion, telefono_padre]
    archivo = "base_matricula.csv"
    with open(archivo, 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(datos)
    messagebox.showinfo("Matriculación Exitosa", "El alumno se ha matriculado correctamente.")
    ventana_matricula.destroy()  

def matricula():
    ventana_matricula = tk.Toplevel()
    ventana_matricula.geometry("900x600")
    ventana_matricula.title("Sección de Matrícula")
    
    nombre_var = tk.StringVar()
    dni_var = tk.StringVar()
    fecha_nacimiento_var = tk.StringVar()
    nombre_padre_var = tk.StringVar()
    direccion_var = tk.StringVar()
    telefono_padre_var = tk.StringVar()
    
    label = tk.Label(ventana_matricula, text="Estás en la sección de matrículas", font=("Helvetica", 16, "bold"))
    label.pack(pady=(20, 10))

   
    label = tk.Label(ventana_matricula, text="Nombre del alumno:")
    label.pack()
    entry_nombre = tk.Entry(ventana_matricula, width=40, textvariable=nombre_var)
    entry_nombre.pack()

    
    label = tk.Label(ventana_matricula, text="DNI del alumno:")
    label.pack()
    entry_dni = tk.Entry(ventana_matricula, width=40, textvariable=dni_var)
    entry_dni.pack()

    
    label = tk.Label(ventana_matricula, text="Fecha de nacimiento:")
    label.pack()
    entry_fecha_nacimiento = tk.Entry(ventana_matricula, width=40, textvariable=fecha_nacimiento_var)
    entry_fecha_nacimiento.pack()

   
    label = tk.Label(ventana_matricula, text="Nombre del padre o apoderado:")
    label.pack()
    entry_nombre_padre = tk.Entry(ventana_matricula, width=40, textvariable=nombre_padre_var)
    entry_nombre_padre.pack()

   
    label = tk.Label(ventana_matricula, text="Dirección:")
    label.pack()
    entry_direccion = tk.Entry(ventana_matricula, width=40, textvariable=direccion_var)
    entry_direccion.pack()

   
    label = tk.Label(ventana_matricula, text="Teléfono del apoderado:")
    label.pack()
    entry_telefono_padre = tk.Entry(ventana_matricula, width=40, textvariable=telefono_padre_var)
    entry_telefono_padre.pack()

    button_registrar = tk.Button(ventana_matricula, text="Registrar alumno", command=lambda: accion_matricula(nombre_var, dni_var, fecha_nacimiento_var, nombre_padre_var, direccion_var, telefono_padre_var, ventana_matricula))
    button_registrar.pack(pady=20)

def base_alumnos():
    ventana_base = tk.Toplevel(root)
    ventana_base.geometry("900x600")
    ventana_base.title("Sección base de alumnos")

    label = tk.Label(ventana_base, text="Alumnos Matriculados:", font=("Helvetica", 16, "bold"))
    label.pack(pady=(20, 10))

    texto_desplazado = scrolledtext.ScrolledText(ventana_base, width=70, height=20)
    texto_desplazado.pack(expand=True, fill="both", padx=20)

    try:
        with open("base_matricula.csv", newline="") as archivo:
            lector_csv = csv.reader(archivo)
            for fila in lector_csv:
                texto_desplazado.insert(tk.END, ", ".join(fila) + "\n")
    except FileNotFoundError:
        texto_desplazado.insert(tk.END, "El archivo csv no se encontró.")

def buscar_alumno():
    ventana_buscar = tk.Toplevel(root)
    ventana_buscar.geometry("600x300")
    ventana_buscar.title("Sección para buscar alumno")

    label = tk.Label(ventana_buscar, text="Ingresa el número de DNI a buscar:", font=("Helvetica", 12))
    label.pack(pady=(20, 10))

    buscar_dni_ = tk.StringVar()
    buscar_dni_entry = tk.Entry(ventana_buscar, width=40, textvariable=buscar_dni_)
    buscar_dni_entry.pack()

    resultado_label = tk.Label(ventana_buscar, text="", font=("Helvetica", 12))
    resultado_label.pack(pady=10)

    def accion_buscar():
        dni = buscar_dni_.get()
        if not dni:
            messagebox.showerror("Error", "Por favor, ingresa el número de DNI.")
            return

        try:
            with open("base_matricula.csv", newline="") as archivo:
                lector_csv = csv.reader(archivo)
                buscar = False
                for fila in lector_csv:
                    if dni == fila[1]:
                        buscar = True
                        resultado_label.config(text="Resultado encontrado:\n" + ", ".join(fila))
                        break
                if not buscar:
                    messagebox.showinfo("Resultado", "No se encontró ningún alumno con ese DNI.")
        except FileNotFoundError:
            messagebox.showerror("Error", "El archivo CSV no se encontró.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

    buscar_button = tk.Button(ventana_buscar, text="Buscar", command=accion_buscar)
    buscar_button.pack(pady=10)

    
    cerrar_button = tk.Button(ventana_buscar, text="Cerrar", command=ventana_buscar.destroy)
    cerrar_button.pack(pady=10)

def eliminar_alumno():
    ventana_eliminar = tk.Toplevel(root)
    ventana_eliminar.geometry("600x300")
    ventana_eliminar.title("Sección para eliminar alumno")

    label = tk.Label(ventana_eliminar, text="Ingresa el número de DNI del alumno a eliminar:", font=("Helvetica", 12))
    label.pack(pady=(20, 10))

    eliminar_dni_ = tk.StringVar()
    eliminar_dni_entry = tk.Entry(ventana_eliminar, width=40, textvariable=eliminar_dni_)
    eliminar_dni_entry.pack()

    def accion_eliminar():
        dni = eliminar_dni_.get() 
        try:
            with open("base_matricula.csv", "r") as archivo:
                lineas = archivo.readlines()

            with open("base_matricula.csv", "w") as archivo:
                eliminado = False
                for linea in lineas:
                    if dni not in linea:
                        archivo.write(linea)
                    else:
                        eliminado = True
                if eliminado:
                    messagebox.showinfo("Eliminación exitosa", "El alumno ha sido eliminado correctamente.")
                else:
                    messagebox.showinfo("Eliminación fallida", "No se encontró ningún alumno con ese DNI.")
                ventana_eliminar.destroy()  
        except FileNotFoundError:
            messagebox.showerror("Error", "El archivo CSV no se encontró.")

    eliminar_button = tk.Button(ventana_eliminar, text="Eliminar", command=accion_eliminar)
    eliminar_button.pack(pady=10)

    cerrar_button = tk.Button(ventana_eliminar, text="Cerrar", command=ventana_eliminar.destroy)
    cerrar_button.pack(pady=10)

root = tk.Tk()
root.geometry("900x600")
root.title("Sistema de Matrículas Escolares")

label = tk.Label(root, text="Institución Educativa Pública General Emilio Soyer Cabero", font=("Helvetica", 20, "bold"))
label.pack(pady=30)

secciones_matricula = tk.Frame(root)
secciones_matricula.pack()

seccion_botones = tk.Frame(root)
seccion_botones.pack()

button1 = tk.Button(seccion_botones, text="Matricular alumno", command=matricula)
button1.pack(side=tk.LEFT, padx=10)

button2 = tk.Button(seccion_botones, text="Base de alumnos registrados", command=base_alumnos)
button2.pack(side=tk.LEFT, padx=10)

button3 = tk.Button(seccion_botones, text="Buscar alumnos", command=buscar_alumno)
button3.pack(side=tk.LEFT, padx=10)

button4 = tk.Button(seccion_botones, text="Eliminar alumno", command=eliminar_alumno)
button4.pack(side=tk.LEFT, padx=10)

root.mainloop()
