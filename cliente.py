import flet as ft
import mysql.connector
from Vehiculo import Herramienta_Vehiculo

def conectar_bd():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="TallerMecanico"
    )


def get_options():
    with conectar_bd() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT cod_Cliente FROM Cliente ORDER BY cod_Cliente")
            resultados = cursor.fetchall()
            return [ft.dropdown.Option(nombre[0]) for nombre in resultados]

def obtener_Cliente_filtrada(nombre):
    with conectar_bd() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT c.cod_Cliente, p.dni, p.nombre, p.apellido, p.tel, p.dir
                FROM Cliente c
                JOIN Persona p ON c.dni_Cliente = p.dni
                WHERE c.cod_Cliente LIKE %s
            """, (nombre,))
            return cursor.fetchall()

def obtener_Cliente():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.cod_Cliente, p.dni, p.nombre, p.apellido, p.tel, p.dir
        FROM Cliente c
        JOIN Persona p ON c.dni_Cliente = p.dni
    """)
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    return resultados

def insertar_Cliente(dni, nombre, apellido, tel, dir_):
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Persona (dni, nombre, apellido, tel, dir) VALUES (%s, %s, %s, %s, %s)",
                       (dni, nombre, apellido, tel, dir_))
        cursor.execute("INSERT INTO Cliente (dni_Cliente) VALUES (%s)",
                       (dni,))
        conn.commit()
    except Exception as e:
        print("Error al insertar Cliente:", e)
    finally:
        cursor.close()
        conn.close()



def eliminar_Cliente(c):
    
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Cliente WHERE dni_Cliente = %s", (c[1],))
        cursor.execute("DELETE FROM Persona WHERE dni = %s", (c[1],))
        conn.commit()
    except Exception as e:
        print("Error al eliminar Cliente:", e)
    finally:
        cursor.close()
        conn.close()

def actualizar_Cliente(dni, nombre, apellido, tel, dir_):
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE Persona SET nombre=%s, apellido=%s, tel=%s, dir=%s WHERE dni=%s
        """, (nombre, apellido, tel, dir_, dni))
        conn.commit()
    except Exception as e:
        print("Error al actualizar Cliente:", e)
    finally:
        cursor.close()
        conn.close()

def Herramienta_Cliente(page: ft.Page):

    
    page.title = "Gestion de Cliente"
    page.scroll = ft.ScrollMode.AUTO

    nombre = ft.TextField(label="Nombre")
    apellido = ft.TextField(label="Apellido")
    dni = ft.TextField(label="DNI")
    telefono = ft.TextField(label="Telefono")
    direccion = ft.TextField(label="Direccion")
    modo_edicion = ft.Text() 

    btn_guardar = ft.ElevatedButton("Guardar")
    btn_cancelar = ft.TextButton("Cancelar")

    form = ft.Column(
        controls=[dni, nombre, apellido, telefono, direccion, ft.Row([btn_guardar, btn_cancelar])],
        visible=False
    )
    tabla = ft.Column()

    filtro = ft.Dropdown(
        border=ft.InputBorder.UNDERLINE,
        editable=True,
        label="Filtro",
        options=get_options(),
    )


    def cargar_tabla(Cliente=None):
        datos = Cliente
        if Cliente is None:
            datos= obtener_Cliente()
        tabla.controls.clear()
        for c in datos:
                tabla.controls.append(ft.Row([
                        ft.Checkbox(value=False,on_change=lambda e, c=c:checkbox_changed(e,c)),
                        ft.Text(str(c[0])),
                        ft.Text(str(c[1])),
                        ft.Text(str(c[2])),
                        ft.Text(str(c[3])),
                        ft.Text(str(c[4])),
                        ft.Text(str(c[5])),
                        
                        ft.Row([
                                ft.IconButton(ft.Icons.EDIT, on_click=lambda e, c=c: mostrar_formulario(c)),
                                ft.IconButton(ft.Icons.DELETE, on_click=lambda e, c=c: eliminar_ui(c)),
                            ]),
                    
                ])
            )
        page.update()

    def checkbox_changed(e, c):
        if e.control.value:  
            for row in tabla.controls:
                checkbox = row.controls[0] 
                checkbox.disabled = True
            e.control.disabled = False 
            Row.controls.append(Herramienta_Vehiculo(page,c))
            page.update()
        else:
            Row.controls.pop(-1)
            page.update()
            for row in tabla.controls:
                checkbox = row.controls[0]
                checkbox.disabled = False
        tabla.update()
        
    def filtrar_tabla(e):
        if filtro.value:
            datos = obtener_Cliente_filtrada(filtro.value)
            filtro.value = ""
            cargar_tabla(datos)
        else:
            cargar_tabla()

    def actualizar_opciones():
        filtro.options = get_options()
        page.update

    def mostrar_formulario(C=None):
        form.visible = True
        if C:
            dni.value = C[1]
            nombre.value = C[2]
            apellido.value = C[3]
            telefono.value = C[4]
            direccion.value = C[5]
            dni.disabled = True
            modo_edicion.value = "editar"
        else:
            dni.value = nombre.value = apellido.value = telefono.value = direccion.value = ""
            dni.disabled = False
            modo_edicion.value = ""
        page.update()

    def enviar_datos(e):
        if modo_edicion.value == "editar":
            actualizar_Cliente(dni.value, nombre.value, apellido.value, telefono.value, direccion.value)
        else:
            insertar_Cliente(dni.value, nombre.value, apellido.value, telefono.value, direccion.value)
        form.visible = False
        filtro.options = get_options()
        cargar_tabla()
        page.update()

    def eliminar_ui(c):
        
        eliminar_Cliente(c)
        actualizar_opciones()
        cargar_tabla()

    def cancelar(e):
        form.visible = False
        page.update()

    btn_guardar.on_click = enviar_datos
    btn_cancelar.on_click = cancelar

    lupa = ft.IconButton(tooltip="Filtrar", icon=ft.Icons.SEARCH, on_click=filtrar_tabla)
    
    Row=ft.Row([tabla])
    
    page.add(
        ft.Text("Cliente", size=24, weight="bold"),
        ft.ElevatedButton("Agregar Cliente", on_click=lambda e: mostrar_formulario()),
        form,
        ft.Divider(),
        ft.Row([filtro, lupa]),
        Row)

    cargar_tabla()

if __name__ == "__Herramienta_Cliente__":
    ft.app(target=Herramienta_Cliente)
