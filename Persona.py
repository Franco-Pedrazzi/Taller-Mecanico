import flet as ft
import mysql.connector

class Persona:
    def __init__(self, DNI, nombre, apellido, telefono, dir):
        self.DNI = DNI
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.dir = dir

def conectar_bd():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            port=3306,
            user='root',
            password='123456',
            database='TallerMecanico',
            ssl_disabled=True
        )
        if connection.is_connected():
            print("Conexión exitosa")
            return connection
    except Exception as e:
        print("Error al conectar a la base de datos:", e)
        return None

def Herramienta_persona(page: ft.Page, main_menu):
    page.title = "Formulario Persona"

    dni = ft.TextField(label="DNI")
    nombre = ft.TextField(label="Nombre")
    apellido = ft.TextField(label="Apellido")
    dir = ft.TextField(label="Dirección")
    tel = ft.TextField(label="Teléfono")

    def enviar(e):
        persona = Persona(
            DNI=dni.value,
            nombre=nombre.value,
            apellido=apellido.value,
            telefono=tel.value,
            dir=dir.value
        )

        conexion = conectar_bd()
        if not conexion:
            page.add(ft.Text("Error de conexión a la base de datos"))
            page.update()
            return

        try:
            cursor = conexion.cursor()
            insert_query = "INSERT INTO Persona (dni, apellido, nombre, dir, tel) VALUES (%s, %s, %s, %s, %s)"
            data = (persona.DNI, persona.apellido, persona.nombre, persona.dir, persona.telefono)
            cursor.execute(insert_query, data)
            conexion.commit()
            page.add(ft.Text("Persona insertada correctamente"))
        except Exception as ex:
            page.add(ft.Text(f"Error al insertar: {ex}"))
        finally:
            cursor.close()
            conexion.close()

        page.update()

    page.add(
        dni,
        nombre,
        apellido,
        dir,
        tel,
        ft.ElevatedButton(text="Guardar Persona", on_click=enviar)
    )