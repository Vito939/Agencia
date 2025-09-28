import tkinter as tk
from tkinter import messagebox
import mysql.connector

#Funcion que extrae el numero ID de una cadena
def extraer_numero_id(cadena):
    # Divide la cadena usando ',' como separador
    valores = cadena.split(',')
    # Itera sobre los valores para encontrar el que contiene "ID"
    for valor in valores:
        if "ID" in valor:
            # Extrae el número después de "ID" y lo convierte a entero para usarse
            numero_id = int(valor.split(':')[1].strip())
            return numero_id

#se define la clase principal de la aplicacion
class AgenciaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Agencias Especiales")
        
        self.root.grid_columnconfigure(1, weight=1) 
        self.root.grid_rowconfigure(4, weight=1)
        # Configuración de la conexión a la base de datos
        self.db_config = {
            'user': 'root',
            'password': '',
            'host': 'localhost',
            'database': 'semana_8'
        }
        # Crea una conexión con la base de datos con excepción en caso de error
        try:
            self.connection = mysql.connector.connect(**self.db_config)
            # Crea un objeto cursor para ejecutar las consultas SQL
            self.cursor = self.connection.cursor()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al conectar a la base de datos: {str(err)}")
            self.root.destroy()
            return
        
        # Crear y configurar los elementos de la interfaz gráfica para Agencia Especial
        self.label_id = tk.Label(root, text="ID de la Agencia:")
        self.entry_id = tk.Entry(root)
        
        self.label_nombre = tk.Label(root, text="Nombre de la Agencia:")
        self.entry_nombre = tk.Entry(root)
        
        self.label_pais = tk.Label(root, text="País:")
        self.entry_pais = tk.Entry(root)
        
        self.label_fecha = tk.Label(root, text="Fecha de Creación (YYYY-MM-DD):")
        self.entry_fecha = tk.Entry(root)
        
        self.btn_agregar = tk.Button(root, text="Agregar Agencia", command=self.agregar_agencia)
        self.btn_mostrar = tk.Button(root, text="Mostrar Agencias", command=self.mostrar_agencias)
        self.btn_borrar = tk.Button(root, text="Borrar Agencia", command=self.borrar_agencia)
        self.btn_actualizar = tk.Button(root, text="Actualizar Agencia", command=self.actualizar_agencia)
        
        # Lista para almacenar información de agencias mostradas
        self.lista_agencias = tk.Listbox(root, selectmode=tk.SINGLE, width=70)
        self.lista_agencias.bind('<<ListboxSelect>>', self.cargar_datos_seleccionados)
        
        # Da estilo a la interfaz grafica, se aplica sticky para un tamaño responsivo y más padding
        padding_args = {'padx': 20, 'pady': 12}
        self.label_id.grid(row=0, column=0, sticky='w', **padding_args)
        self.entry_id.grid(row=0, column=1, sticky='ew', **padding_args)
        self.label_nombre.grid(row=1, column=0, sticky='w', **padding_args)
        self.entry_nombre.grid(row=1, column=1, sticky='ew', **padding_args)
        self.label_pais.grid(row=2, column=0, sticky='w', **padding_args)
        self.entry_pais.grid(row=2, column=1, sticky='ew', **padding_args)
        self.label_fecha.grid(row=3, column=0, sticky='w', **padding_args)
        self.entry_fecha.grid(row=3, column=1, sticky='ew', **padding_args)
        self.lista_agencias.grid(row=4, column=0, columnspan=2, sticky='nsew', padx=20, pady=16)
        self.btn_agregar.grid(row=5, column=0, columnspan=1, sticky='ew', padx=20, pady=12)
        self.btn_mostrar.grid(row=5, column=1, columnspan=1, sticky='ew', padx=20, pady=12)
        self.btn_borrar.grid(row=6, column=0, columnspan=1, sticky='ew', padx=20, pady=12)
        self.btn_actualizar.grid(row=6, column=1, columnspan=1, sticky='ew', padx=20, pady=12)
        self.mostrar_agencias()  # Mostrar agencias al iniciar la aplicación

    def agregar_agencia(self):
        agencia_id = self.entry_id.get()
        nombre = self.entry_nombre.get()
        pais = self.entry_pais.get()
        fecha = self.entry_fecha.get()
        try:
            # Insertar datos en la tabla
            query = "INSERT INTO Agencias (ID, Nombre, Pais, FechaCreacion) VALUES (%s, %s, %s, %s)"
            values = (agencia_id, nombre, pais, fecha)
            self.cursor.execute(query, values)
            # Confirmar la transacción
            self.connection.commit()
            messagebox.showinfo("Éxito", "Agencia agregada correctamente")
            self.limpiar_campos()
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar agencia: {str(e)}")

    def mostrar_agencias(self):
        try:
            # Limpiar la lista de agencias antes de mostrarlas
            self.lista_agencias.delete(0, tk.END)
            # Realizar una consulta SELECT
            query = "SELECT * FROM Agencias"
            self.cursor.execute(query)
            # Obtener todos los resultados
            agencias = self.cursor.fetchall()
            # Mostrar los resultados en la lista
            for agencia in agencias:
                self.lista_agencias.insert(tk.END, f"ID: {agencia[0]}, Nombre: {agencia[1]}, País: {agencia[2]}, Fecha: {agencia[3]}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar agencias: {str(e)}")

    def borrar_agencia(self):
        try:
            seleccion = self.lista_agencias.curselection()
            if seleccion:
                agencia_seleccionada = self.lista_agencias.get(seleccion[0])
                agencia_id = extraer_numero_id(agencia_seleccionada)
                # Borrar agencia de la base de datos
                query = "DELETE FROM Agencias WHERE ID = %s"
                self.cursor.execute(query, (agencia_id,))
                # Confirmar la transacción
                self.connection.commit()
                messagebox.showinfo("Éxito", f"Agencia con ID {agencia_id} borrada correctamente")
                self.mostrar_agencias()
                self.limpiar_campos()
        except Exception as e:
            messagebox.showerror("Error", f"Error al borrar agencia: {str(e)}")

    def cargar_datos_seleccionados(self, event):
        seleccion = self.lista_agencias.curselection()
        if seleccion:
            agencia_seleccionada = self.lista_agencias.get(seleccion[0])
            agencia_id = extraer_numero_id(agencia_seleccionada)
            # Obtener datos de la agencia seleccionada
            query = "SELECT * FROM Agencias WHERE ID = %s"
            self.cursor.execute(query, (agencia_id,))
            datos_agencia = self.cursor.fetchone()
            # Cargar datos en los campos de entrada
            self.entry_id.delete(0, tk.END)
            self.entry_id.insert(0, datos_agencia[0])
            self.entry_nombre.delete(0, tk.END)
            self.entry_nombre.insert(0, datos_agencia[1])
            self.entry_pais.delete(0, tk.END)
            self.entry_pais.insert(0, datos_agencia[2])
            self.entry_fecha.delete(0, tk.END)
            self.entry_fecha.insert(0, datos_agencia[3])

    def actualizar_agencia(self):
        try:
            seleccion = self.lista_agencias.curselection()
            agencia_id = self.entry_id.get()
            nombre = self.entry_nombre.get()
            pais = self.entry_pais.get()
            fecha = self.entry_fecha.get()
            # Actualizar agencia en la base de datos
            query = "UPDATE Agencias SET Nombre = %s, Pais = %s, FechaCreacion = %s WHERE ID = %s"
            values = (nombre, pais, fecha, agencia_id)
            self.cursor.execute(query, values)
            # Confirmar la transacción
            self.connection.commit()
            messagebox.showinfo("Éxito", f"Agencia con ID {agencia_id} actualizada correctamente")
            self.mostrar_agencias()
            self.limpiar_campos()
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar agencia: {str(e)}")

    def limpiar_campos(self):
        self.entry_id.delete(0, tk.END)
        self.entry_nombre.delete(0, tk.END)
        self.entry_pais.delete(0, tk.END)
        self.entry_fecha.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = AgenciaApp(root)
    root.mainloop()
    # Cerrar el cursor y la conexión al cerrar la aplicación
    app.cursor.close()
    app.connection.close()
