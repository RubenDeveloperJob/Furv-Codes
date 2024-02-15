# This is a sample Python script.
import os
# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import tkinter as tk
import subprocess
from tkinter import filedialog, simpledialog
from PIL import Image, ImageTk
from datetime import datetime
CONTRASENA = "abcd"


def generar_codigo():
    global codigo

    # Obtener los valores de los campos
    año = año_var.get()[-2:]
    tipo_equipo = tipo_equipo_var.get()
    marca = marca_var.get()
    empresa = empresa_var.get()
    seccion = seccion_var.get()
    serie = serie_entry.get()[-6:]


    # Obtener el código numérico asociado a la empresa y la sección
    try:
        nombre_empresa_sin_numero = empresa.split(",")[0]
        nombre_seccion_sin_numero = seccion.split(",")[0]
        tipo_equipo_sin_numero = tipo_equipo.split(",")[0]

        codigo_empresa = obtener_codigo_empresa(nombre_empresa_sin_numero)
        codigo_seccion = obtener_codigo_seccion(nombre_seccion_sin_numero)
        tipo_equipo = obtener_codigo_tipoequipo(tipo_equipo_sin_numero)
    except:
        # En caso de error, asignar ### como valor predeterminado
        codigo_empresa = codigo_seccion = tipo_equipo = "###"

    # Generar el código con las variables actualizadas
    codigo = f"{codigo_empresa}{año}{codigo_seccion}{tipo_equipo}-{serie} "
    print("codigo: ")
    print(codigo)
    codigos_listbox.insert(tk.END, codigo)


def obtener_codigo_empresa(nombre_empresa):
    print(nombre_empresa)
    with open("empresas.txt", "r") as file:
        for linea in file:
            partes = linea.strip().split(",")
            print(partes)
            if partes[0].strip() == nombre_empresa.strip():  # Aquí se realizan los cambios
                return partes[1]
    raise ValueError(f"No se encontró el código numérico para '{nombre_empresa}' en el archivo 'empresas.txt'.")


def obtener_codigo_tipoequipo(nombre_tipo):
    print(nombre_tipo)
    with open("equipos.txt", "r") as file:
        for linea in file:
            partes = linea.strip().split(",")
            if partes[0].strip() == nombre_tipo.strip():  # Aquí se realizan los cambios
                return partes[1]
    raise ValueError(f"No se encontró el código numérico para '{nombre_tipo}' en el archivo 'secciones.txt'.")


def obtener_codigo_seccion(nombre_seccion):
    print(nombre_seccion)
    with open("secciones.txt", "r") as file:
        for linea in file:
            partes = linea.strip().split(",")
            if partes[0].strip() == nombre_seccion.strip():  # Aquí se realizan los cambios
                return partes[1]
    raise ValueError(f"No se encontró el código numérico para '{nombre_seccion}' en el archivo 'secciones.txt'.")


def cargar_opciones_desde_archivo(archivo):
    opciones = []
    with open(archivo, "r") as file:
        for linea in file:
            opciones.append(linea.strip())
    return opciones


def obtener_codigo_numerico(nombre, archivo):
    with open(archivo, "r") as file:
        for linea in file:
            partes = linea.strip().split(",")
            if partes[0] == nombre:
                return partes[1]
    raise ValueError(f"No se encontró el código numérico para '{nombre}' en el archivo '{archivo}'.")


def abrir_archivo_opciones():
    ruta_archivo = filedialog.askopenfilename(filetypes=[("equipos", "*.txt")])
    if ruta_archivo:
        with open(ruta_archivo, "r") as archivo:
            opciones = archivo.read()
            # Aquí puedes procesar las opciones como desees
            print(opciones)


# Crear la ventana principal
ventana = tk.Tk()
ventana.title("ITFURV CODE")
ventana.iconbitmap("logo-urv.ico")
ventana.geometry("780x500")

# Definir colores personalizados
color_fondo = "#F5F5F5"
color_marco = "#E0E0E0"
color_botones = "#4CAF50"
color_texto = "#212121"

# Configurar colores de fondo
ventana.configure(bg=color_fondo)

# Crear un marco para contener todos los widgets
marco_principal = tk.Frame(ventana, bg=color_marco, bd=5, relief="groove", padx=20, pady=20)
marco_principal.place(relx=0.5, rely=0.5, anchor="center")

# Widgets de la interfaz
logo = Image.open("urvimg.png")
logo = logo.resize((160, 48))
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(marco_principal, image=logo, bg=color_marco)
logo_label.grid(row=0, column=0, columnspan=1, pady=(0, 10))

opciones_año = [str(año) for año in range(2000, datetime.now().year + 1)]
año_var = tk.StringVar(ventana)
tipo_equipo_var = tk.StringVar(ventana)  # Variable para la selección de tipo equipo
marca_var = tk.StringVar(ventana)  # Variable para la selección de marca
empresa_var = tk.StringVar(ventana)  # Variable para la selección de la empresa
seccion_var = tk.StringVar(ventana)  # Variable para la selección de la sección

año_label = tk.Label(marco_principal, text="Año:", bg=color_marco, fg=color_texto)
año_label.grid(row=1, column=0, padx=5, pady=5)
año_menu = tk.OptionMenu(marco_principal, año_var, *opciones_año)

tipo_equipo_label = tk.Label(marco_principal, text="Tipo de Equipo:", bg=color_marco, fg=color_texto)
marca_label = tk.Label(marco_principal, text="Marca:", bg=color_marco, fg=color_texto)
empresa_label = tk.Label(marco_principal, text="Empresa:", bg=color_marco, fg=color_texto)
seccion_label = tk.Label(marco_principal, text="Sección:", bg=color_marco, fg=color_texto)

# Listbox y barras de desplazamiento
codigos_listbox = tk.Listbox(marco_principal, width=60, height=10, bg=color_marco, fg=color_texto)
codigos_listbox.grid(row=1, column=2, rowspan=8, padx=5, pady=5, sticky="nsew")

scrollbar_vertical = tk.Scrollbar(marco_principal, orient="vertical", command=codigos_listbox.yview)
scrollbar_vertical.grid(row=1, column=3, rowspan=8, sticky="ns")
codigos_listbox.config(yscrollcommand=scrollbar_vertical.set)

scrollbar_horizontal = tk.Scrollbar(marco_principal, orient="horizontal", command=codigos_listbox.xview)
scrollbar_horizontal.grid(row=9, column=2, sticky="ew")  # Ajustar la posición de la barra horizontal
codigos_listbox.config(xscrollcommand=scrollbar_horizontal.set)

imagen_ajustes = Image.open("ajustes.png")  # Cambia "icono_ajustes.png" por el nombre de tu archivo de imagen
imagen_ajustes = imagen_ajustes.resize((20, 20))  # Ajusta el tamaño de la imagen según tus necesidades
imagen_ajustes = ImageTk.PhotoImage(imagen_ajustes)

#boton_ajustes = tk.Button(ventana, image=imagen_ajustes, command=abrir_archivo_opciones, bd=0)
#boton_ajustes.pack(side=tk.TOP, anchor=tk.NW, padx=3, pady=3)
def abrir_archivo_con_notepad(nombre_archivo):
    try:
        # Abrir el archivo con el bloc de notas
        subprocess.run(["notepad.exe", f"{nombre_archivo}.txt"])
    except FileNotFoundError:
        print(f"No se pudo abrir el archivo {nombre_archivo}.txt.")

def seleccionar_opcion(opcion):
    if opcion == "Empresas":
        abrir_archivo_con_notepad("empresas")
    elif opcion == "Secciones":
        abrir_archivo_con_notepad("secciones")
    elif opcion == "Equipos":
        abrir_archivo_con_notepad("equipos")
    elif opcion == "Marca":
        abrir_archivo_con_notepad("marcas")

# Lista de opciones para el menú desplegable
opciones_archivos = ["Empresas", "Secciones", "Equipos", "Marcas"]

# Función para abrir el menú desplegable
def abrir_menu():
    # Solicitar la contraseña
    contraseña = simpledialog.askstring("Contraseña", "Introduce la contraseña:", show='*')
    # Verificar si la contraseña es correcta
    if contraseña == CONTRASENA:
        # Desplegar el menú de opciones
        menu_archivos.tk_popup(botones_ajustes.winfo_rootx(), botones_ajustes.winfo_rooty() + botones_ajustes.winfo_height())
    else:
        # Mostrar un mensaje de error si la contraseña es incorrecta
        tk.messagebox.showerror("Error", "Contraseña incorrecta. Inténtalo de nuevo.")

def abrir_info():
    tk.messagebox.showwarning("Información",
                              "El formato de los ficheros de configuración son:\n\n"
                              "NOMBRE DEL ELEMENTO, NOMENCLATURA CÓDIGO\n\n"
                              "La aplicación es autoportable, por lo que no cuenta con una base de datos.\n"
                              "Si tiene algún problema, contacte con el administrador.\n"
                              "Si hace algún cambio debe refrescar: ♻")

def refrescar():
    _empresas = cargar_opciones_desde_archivo("empresas.txt")
    _secciones = cargar_opciones_desde_archivo("secciones.txt")
    _marcas = cargar_opciones_desde_archivo("marcas.txt")
    _equipos = cargar_opciones_desde_archivo("equipos.txt")
    equipo_menu = tk.OptionMenu(marco_principal, tipo_equipo_var, *_equipos)
    equipo_menu.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

    marca_menu = tk.OptionMenu(marco_principal, marca_var, *_marcas)
    marca_menu.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

    empresa_menu = tk.OptionMenu(marco_principal, empresa_var, *_empresas)
    empresa_menu.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

    seccion_menu = tk.OptionMenu(marco_principal, seccion_var, *_secciones)
    seccion_menu.grid(row=5, column=1, padx=5, pady=5, sticky="ew")

def guardar():
    # Obtener todos los elementos de la Listbox
    codigos = codigos_listbox.get(0, tk.END)

    # Abrir el diálogo para seleccionar la ubicación y el nombre del archivo
    ruta_archivo = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de texto", "*.txt")])

    # Verificar si se seleccionó un archivo
    if ruta_archivo:
        # Escribir los códigos en el archivo seleccionado
        with open(ruta_archivo, "w") as file:
            for codigo in codigos:
                file.write(codigo + "\n")

        print(f"Los códigos se han guardado en el archivo '{ruta_archivo}'.")

# Crear el botón de ajustes
botones_ajustes = tk.Button(ventana, text="⚙️", command=abrir_menu)
botones_ajustes.pack(side=tk.TOP, anchor=tk.NW, padx=1, pady=0)

# Crear el botón de Informacion
botones_info = tk.Button(ventana, text="👤❓", command=abrir_info)
botones_info.place(x=30, y=0)

botones_refres = tk.Button(ventana, text="♻", command=refrescar)
botones_refres.place(x=65, y=0)

botones_export = tk.Button(ventana, text="⏬",command=guardar)
botones_export.place(x=95, y=0)

# Crear el menú desplegable
menu_archivos = tk.Menu(ventana, tearoff=False)
for opcion in opciones_archivos:
    menu_archivos.add_command(label=opcion, command=lambda o=opcion: seleccionar_opcion(o))


# Crear el menú desplegable


# Llamada a la función para cargar opciones de empresas y secciones desde el archivo "empresas_secciones_codigos.txt"
_empresas = cargar_opciones_desde_archivo("empresas.txt")
_secciones = cargar_opciones_desde_archivo("secciones.txt")
_marcas = cargar_opciones_desde_archivo("marcas.txt")
_equipos = cargar_opciones_desde_archivo("equipos.txt")

# Posicionar los widgets en el marco
año_label.grid(row=1, column=0, sticky="w")
año_menu.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
tipo_equipo_label.grid(row=2, column=0, sticky="w")
marca_label.grid(row=3, column=0, sticky="w")
empresa_label.grid(row=4, column=0, sticky="w")
seccion_label.grid(row=5, column=0, sticky="w")

equipo_menu = tk.OptionMenu(marco_principal, tipo_equipo_var, *_equipos)
equipo_menu.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

marca_menu = tk.OptionMenu(marco_principal, marca_var, *_marcas)
marca_menu.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

empresa_menu = tk.OptionMenu(marco_principal, empresa_var, *_empresas)
empresa_menu.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

seccion_menu = tk.OptionMenu(marco_principal, seccion_var, *_secciones)
seccion_menu.grid(row=5, column=1, padx=5, pady=5, sticky="ew")

serie_label = tk.Label(marco_principal, text="Número de serie:", bg=color_marco, fg=color_texto)
serie_entry = tk.Entry(marco_principal)
serie_label.grid(row=6, column=0, pady=(10, 0), sticky="w")
serie_entry.grid(row=6, column=1, padx=5, pady=(10, 0), sticky="ew")

generar_boton = tk.Button(marco_principal, text="Generar Código", command=generar_codigo, width=15, bg=color_botones)
generar_boton.grid(row=7, column=1, padx=5, pady=(10, 0), sticky="ew")

# Ejecutar la ventana
ventana.mainloop()

