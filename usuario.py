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
            cursor.execute("SELECT email FROM Usuarios ORDER BY email")
            resultados = cursor.fetchall()
            return [ft.dropdown.Option(email[0]) for email in resultados]

def obtener_Usuario_filtrada(email):
    with conectar_bd() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT email, nombre, contraseña
                FROM Usuarios
                WHERE email LIKE %s
            """, (f"%{email}%",))
            return cursor.fetchall()

def obtener_Usuario():
    with conectar_bd() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT email, nombre, contraseña FROM Usuarios")
            return cursor.fetchall()

def insertar_Usuario(email, nombre, contraseña):
    with conectar_bd() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO Usuarios (email, nombre, contraseña)
                VALUES (%s, %s, %s)
            """, (email, nombre, contraseña))
            conn.commit()

def eliminar_Usuario(email):
    with conectar_bd() as conn:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM Usuarios WHERE email = %s", (email,))
            conn.commit()

def actualizar_Usuario(email, nombre, contraseña):
    with conectar_bd() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE Usuarios
                SET nombre=%s, contraseña=%s
                WHERE email=%s
            """, (nombre, contraseña, email))
            conn.commit()

def Herramienta_Usuario(page: ft.Page):
    page.title = "Gestion de Usuarios"
    page.scroll = ft.ScrollMode.AUTO

    email = ft.TextField(label="email")
    nombre = ft.TextField(label="nombre")
    contraseña = ft.TextField(label="contraseña")
    modo_edicion = ft.Text()

    btn_guardar = ft.ElevatedButton("Guardar")
    btn_cancelar = ft.TextButton("Cancelar")

    form = ft.Column(
        controls=[email, nombre, contraseña, ft.Row([btn_guardar, btn_cancelar])],
        visible=False
    )

    tabla = ft.Column()

    filtro = ft.Dropdown(
        border=ft.InputBorder.UNDERLINE,
        editable=True,
        label="Filtro",
        options=get_options(),
    )

    def actualizar_opciones():
        filtro.options = get_options()
        page.update()

    def cargar_tabla(Usuario=None):
        datos = Usuario
        if Usuario is None:
            datos= obtener_Usuario()
        tabla.controls.clear()
        for c in datos:
                tabla.controls.append(ft.Row([
                        ft.Text(str(c[0])),
                        ft.Text(str(c[1])),
                        
                        ft.Row([
                                ft.IconButton(ft.Icons.EDIT, on_click=lambda e, c=c: mostrar_formulario(c)),
                                ft.IconButton(ft.Icons.DELETE, on_click=lambda e, email=c[0]: eliminar_ui(email)),
                            ]),
                    
                ])
            )
        page.update()

    def filtrar_tabla(e):
        if filtro.value:
            datos = obtener_Usuario_filtrada(filtro.value)
            filtro.value = ""
            cargar_tabla(datos)
        else:
            cargar_tabla()

    def mostrar_formulario(Usuario=None):
        form.visible = True
        if Usuario:
            email.value = Usuario[0]
            nombre.value = str(Usuario[1])
            contraseña.value = str(Usuario[2])
            email.disabled = True
            modo_edicion.value = "editar"
        else:
            email.value = nombre.value = contraseña.value = ""
            modo_edicion.value = ""
            email.disabled = False
        page.update()

    def enviar_datos(e):
        if not email.value.strip():
            page.update()
            return

        try:
            nombre_val = str(nombre.value)
            contraseña_val = int(contraseña.value)

        except ValueError:
            page.update()
            return

        if modo_edicion.value == "editar":
            actualizar_Usuario(email.value, nombre_val, contraseña_val)
        else:
            insertar_Usuario(email.value, nombre_val, contraseña_val)
        filtro.options=get_options()
         
        form.visible = False
        cargar_tabla()

    def eliminar_ui(email):
        eliminar_Usuario(email)
        actualizar_opciones()
        cargar_tabla()

    def cancelar(e):
        form.visible = False
        page.update()

    btn_guardar.on_click = enviar_datos
    btn_cancelar.on_click = cancelar

    lupa = ft.IconButton(tooltip="Filtrar", icon=ft.Icons.SEARCH, on_click=filtrar_tabla)

    page.add(
        ft.Text("Usuarios", size=24, weight="bold"),
        ft.ElevatedButton("Agregar Usuario", on_click=lambda e: mostrar_formulario()),
        form,
        ft.Divider(),
        ft.Row([filtro, lupa]),
        tabla
    )

    cargar_tabla()


if __name__ == "__main__":
    ft.app(target=Herramienta_Usuario)