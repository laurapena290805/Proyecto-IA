import tkinter as tk
from tkinter import filedialog, messagebox

from Busquedas import ejecutar_busquedas



class PantallaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Agente Ratón")
        self.geometry("600x700")
        

        self.matriz = None  # Aquí guardaremos la matriz cargada
        self.nombre_archivo = None
        self.marco_encabezado()
        self.marco_configuracion()


    def marco_encabezado(self):
        # Encabezado
        marco_encabezado = tk.Frame(self)
        marco_encabezado.pack(fill="x", padx=20, pady=20)
        
        titulo = tk.Label(marco_encabezado, text="Agente Ratón", font=("Arial", 24, "bold"))
        titulo.pack(pady=(10, 5))
        
        subtitulo = tk.Label(marco_encabezado, text="Buscando el queso", font=("Arial", 16))
        subtitulo.pack()
        
        texto_informacion = tk.Label(marco_encabezado, text="¡Bienvenido a Agente Ratón! El raton que busca su queso. Selecciona el mapa(.txt) que deseas utilizar, ingresa los datos necesarios y presiona el botón de inicio para comenzar la búsqueda con algoritmos aleatorios.", wraplength=500, justify="center")
        texto_informacion.pack(pady=(10, 20))


    def marco_configuracion(self):
        # Marco de Configuración
        marco_entrada = tk.Frame(self)
        marco_entrada.pack(pady=10)
        
        """
        # Entrada de Filas y Columnas
        tk.Label(marco_entrada, text="Número de filas (n):").grid(row=0, column=0, padx=10, pady=5)
        self.entrada_filas = tk.Entry(marco_entrada)
        self.entrada_filas.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(marco_entrada, text="Número de columnas (m):").grid(row=1, column=0, padx=10, pady=5)
        self.entrada_columnas = tk.Entry(marco_entrada)
        self.entrada_columnas.grid(row=1, column=1, padx=10, pady=5)
        """
        
        # Entrada de Iteraciones y Profundidad
        tk.Label(marco_entrada, text="Número de iteraciones:").grid(row=2, column=0, padx=10, pady=5)
        self.entrada_iteraciones = tk.Entry(marco_entrada)
        self.entrada_iteraciones.grid(row=2, column=1, padx=10, pady=5)
        
        tk.Label(marco_entrada, text="Número de profundidad:").grid(row=3, column=0, padx=10, pady=5)
        self.entrada_profundidad = tk.Entry(marco_entrada)
        self.entrada_profundidad.grid(row=3, column=1, padx=10, pady=5)

        # Coordenadas de Inicio y Meta
        tk.Label(marco_entrada, text="Coordenadas de Inicio (x, y):").grid(row=4, column=0, padx=10, pady=5)
        self.entrada_coordenadas_inicio = tk.Entry(marco_entrada)
        self.entrada_coordenadas_inicio.grid(row=4, column=1, padx=10, pady=5)

        tk.Label(marco_entrada, text="Coordenadas de Meta (x, y):").grid(row=5, column=0, padx=10, pady=5)
        self.entrada_coordenadas_meta = tk.Entry(marco_entrada)
        self.entrada_coordenadas_meta.grid(row=5, column=1, padx=10, pady=5)

        # Información del Archivo
        self.etiqueta_nombre_archivo = tk.Label(self, text="Archivo no cargado", fg="red")
        self.etiqueta_nombre_archivo.pack()

        #Imprimir la matriz como string
        self.etiqueta_matriz = tk.Label(self, text= self.matriz)
        self.etiqueta_matriz.pack()


        # Botón de Cargar Archivo
        boton_archivo = tk.Button(self, text="Cargar archivo .txt", command=self.cargar_archivo)
        boton_archivo.pack(pady=10)

        # Botón de Continuar
        boton_continuar = tk.Button(self, text="Iniciar", command=self.validacion)
        boton_continuar.pack(pady=20)
        
    def cargar_archivo(self):
        ruta_archivo = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if ruta_archivo:
            with open(ruta_archivo, 'r') as archivo:
                lineas = archivo.readlines()
                matriz = [list(linea.strip()) for linea in lineas if linea.strip()]

            # Mostrar ventana emergente para confirmar la matriz
            self.mostrar_dialogo_matriz(matriz, ruta_archivo)

    def mostrar_dialogo_matriz(self, matriz, ruta_archivo):
        # Crear una ventana emergente
        dialogo = tk.Toplevel(self)
        dialogo.title("Confirmar Matriz Cargada")

        # Mostrar la matriz en la ventana emergente
        etiqueta_matriz = tk.Label(dialogo, text="¿Deseas usar esta matriz?")
        etiqueta_matriz.pack(pady=10)

        for fila in matriz:
            etiqueta_fila = tk.Label(dialogo, text=" ".join(fila), font=("Courier", 12))
            etiqueta_fila.pack()

        # Botones de confirmación
        boton_confirmar = tk.Button(dialogo, text="Confirmar", command=lambda: self.confirmar_matriz(dialogo, matriz, ruta_archivo))
        boton_confirmar.pack(side="left", padx=20, pady=20)

        boton_cancelar = tk.Button(dialogo, text="Cancelar", command=dialogo.destroy)
        boton_cancelar.pack(side="right", padx=20, pady=20)

    def confirmar_matriz(self, dialogo, matriz, ruta_archivo):
        # Actualizar variables y etiquetas
        self.matriz = matriz
        self.nombre_archivo = ruta_archivo.split("/")[-1]
        self.etiqueta_nombre_archivo.config(text=f"Archivo cargado: {self.nombre_archivo}", fg="green")
        #Imprimir la matriz como string linea por linea
        self.etiqueta_matriz.config(text= "\n".join(["".join(fila) for fila in matriz]), font=("Courier", 12))
        # Cerrar el diálogo
        dialogo.destroy()

    def validacion(self):
        # Validación básica de los campos de entrada (puede ampliarse)
        if not self.entrada_iteraciones.get().isdigit() or not self.entrada_profundidad.get().isdigit():
            messagebox.showerror("Error", "Por favor ingrese valores numéricos en iteraciones y profundidad.")
            return
        # Validar las coordenadas de inicio y meta
        try:
            inicio = eval(self.entrada_coordenadas_inicio.get())
            meta = eval(self.entrada_coordenadas_meta.get())
            max_iteraciones = int(self.entrada_iteraciones.get())
            if not (isinstance(inicio, tuple) and isinstance(meta, tuple)):
                raise ValueError
        except:
            messagebox.showerror("Error", "Las coordenadas deben tener el formato (x, y).")
            return
        #validar si se ha cargado un archivo
        if self.matriz is None:
            messagebox.showerror("Error", "Por favor cargue un archivo .txt.")
            return
        
        ejecutar_busquedas(self.matriz, meta, inicio, max_iteraciones)
        

if __name__ == "__main__":
    app = PantallaPrincipal()
    app.mainloop()