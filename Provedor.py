import flet as ft
import mysql.connector

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
            cursor.execute("SELECT cod_Provedor FROM Provedor ORDER BY cod_Provedor")
            resultados = cursor.fetchall()
            return [ft.dropdown.Option(nombre[0]) for nombre in resultados]

def obtener_Provedor_filtrada(nombre):
    with conectar_bd() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT c.cod_Provedor, p.dni, p.nombre, p.apellido, p.tel, p.dir
                FROM Provedor c
                JOIN Persona p ON c.dni_Provedor = p.dni
                WHERE c.cod_Provedor LIKE %s
            """, (nombre,))
            return cursor.fetchall()

def obtener_Provedor():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.cod_Provedor, p.dni, p.nombre, p.apellido, p.tel, p.dir
        FROM Provedor c
        JOIN Persona p ON c.dni_Provedor = p.dni
    """)
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    return resultados

def insertar_Provedor(cod_Provedor, dni, nombre, apellido, tel, dir_):
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Persona (dni, nombre, apellido, tel, dir) VALUES (%s, %s, %s, %s, %s)",
                       (dni, nombre, apellido, tel, dir_))
        cursor.execute("INSERT INTO Provedor (cod_Provedor, dni_Provedor) VALUES (%s, %s)",
                       (cod_Provedor, dni))
        conn.commit()
    except Exception as e:
        print("Error al insertar Provedor:", e)
    finally:
        cursor.close()
        conn.close()



def eliminar_Provedor(c):
    
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Provedor WHERE dni_Provedor = %s", (c[1],))
        cursor.execute("DELETE FROM Persona WHERE dni = %s", (c[1],))
        conn.commit()
    except Exception as e:
        print("Error al eliminar Provedor:", e)
    finally:
        cursor.close()
        conn.close()

def actualizar_Provedor(cod_Provedor, dni, nombre, apellido, tel, dir_):
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE Persona SET nombre=%s, apellido=%s, tel=%s, dir=%s WHERE dni=%s
        """, (nombre, apellido, tel, dir_, dni))
        cursor.execute("""
            UPDATE Provedor SET cod_Provedor=%s WHERE dni_Provedor=%s
        """, (cod_Provedor, dni))
        conn.commit()
    except Exception as e:
        print("Error al actualizar Provedor:", e)
    finally:
        cursor.close()
        conn.close()

def Herramienta_Provedor(page: ft.Page):
    page.title = "Gestion de Provedor"
    page.scroll = ft.ScrollMode.AUTO

    nombre = ft.TextField(label="Nombre")
    apellido = ft.TextField(label="Apellido")
    dni = ft.TextField(label="DNI")
    telefono = ft.TextField(label="Telefono")
    direccion = ft.TextField(label="Direccion")
    codigo = ft.TextField(label="Codigo Provedor")
    modo_edicion = ft.Text() 

    btn_guardar = ft.ElevatedButton("Guardar")
    btn_cancelar = ft.TextButton("Cancelar")

    form = ft.Column(
        controls=[codigo, dni, nombre, apellido, telefono, direccion, ft.Row([btn_guardar, btn_cancelar])],
        visible=False
    )
    tabla = ft.Column()

    filtro = ft.Dropdown(
        border=ft.InputBorder.UNDERLINE,
        editable=True,
        label="Filtro",
        options=get_options(),
    )


    def cargar_tabla(Provedor=None):
        datos = Provedor
        if Provedor is None:
            datos= obtener_Provedor()
        tabla.controls.clear()
        for c in datos:
                tabla.controls.append(ft.Row([
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

    def filtrar_tabla(e):
        if filtro.value:
            datos = obtener_Provedor_filtrada(filtro.value)
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
            codigo.value = C[0]
            dni.value = C[1]
            nombre.value = C[2]
            apellido.value = C[3]
            telefono.value = C[4]
            direccion.value = C[5]
            codigo.disabled = True
            dni.disabled = True
            modo_edicion.value = "editar"
        else:
            codigo.value = dni.value = nombre.value = apellido.value = telefono.value = direccion.value = ""
            codigo.disabled = False
            dni.disabled = False
            modo_edicion.value = ""
        page.update()

    def enviar_datos(e):
        if modo_edicion.value == "editar":
            actualizar_Provedor(codigo.value, dni.value, nombre.value, apellido.value, telefono.value, direccion.value)
        else:
            insertar_Provedor(codigo.value, dni.value, nombre.value, apellido.value, telefono.value, direccion.value)
        form.visible = False
        filtro.options = get_options()
        cargar_tabla()
        page.update()

    def eliminar_ui(c):
        
        eliminar_Provedor(c)
        actualizar_opciones()
        cargar_tabla()

    def cancelar(e):
        form.visible = False
        page.update()

    btn_guardar.on_click = enviar_datos
    btn_cancelar.on_click = cancelar

    lupa = ft.IconButton(tooltip="Filtrar", icon=ft.Icons.SEARCH, on_click=filtrar_tabla)

    page.add(
        ft.Text("Provedor", size=24, weight="bold"),
        ft.ElevatedButton("Agregar Provedor", on_click=lambda e: mostrar_formulario()),
        form,
        ft.Divider(),
        ft.Row([filtro, lupa]),
        tabla
    )

    cargar_tabla()

if __name__ == "__Herramienta_Provedor__":
    ft.app(target=Herramienta_Provedor)
