import flet as ft
import mysql.connector
from classes import Usuarios

def Herramienta_Usuario(page: ft.Page):
    page.title = "Gestion de Usuarios"
    page.scroll = ft.ScrollMode.AUTO

    email = ft.TextField(label="email")
    contraseña = ft.TextField(label="contraseña")
    legajo = ft.Dropdown(
        border=ft.InputBorder.UNDERLINE,
        editable=True,
        label="legajo",
        options=Usuarios.get_options_legajos(),
    )
    modo_edicion = ft.Text()

    btn_guardar = ft.ElevatedButton("Guardar")
    btn_cancelar = ft.TextButton("Cancelar")

    form = ft.Column(
        controls=[legajo,email, contraseña, ft.Row([btn_guardar, btn_cancelar])],
        visible=False
    )

    tabla = ft.Column()

    filtro = ft.Dropdown(
        border=ft.InputBorder.UNDERLINE,
        editable=True,
        label="Filtro",
        options=Usuarios.get_options(),
    )

    def actualizar_opciones():
        filtro.options = Usuarios.get_options()
        page.update()

    def cargar_tabla(Usuario=None):
        datos = Usuario
        if Usuario is None:
            datos= Usuarios.obtener_Usuario()
        tabla.controls.clear()
        for c in datos:
                tabla.controls.append(ft.Row([
                        ft.Text(str(c[3])),
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
            datos = Usuarios.obtener_Usuario_filtrada(filtro.value)
            filtro.value = ""
            cargar_tabla(datos)
        else:
            cargar_tabla()

    def mostrar_formulario(Usuario=None):
        form.visible = True
        if Usuario:
            legajo.value = str(Usuario[3])
            email.value = Usuario[0]
            contraseña.value = str(Usuario[2])
            email.disabled = True
            modo_edicion.value = "editar"
        else:
            email.value = contraseña.value = legajo.value= ""
            modo_edicion.value = ""
            email.disabled = False
        page.update()

    def enviar_datos(e):
        if not email.value:
            page.update()
            return

        try:
            contraseña_val = int(contraseña.value)
            legajo_val = int(legajo.value)
        except ValueError:
            page.update()
            return

        if modo_edicion.value == "editar":
            Usuarios.actualizar_Usuario(email.value, contraseña_val,legajo_val)
        else:
            Usuarios.insertar_Usuario(email.value, contraseña_val,legajo_val)
        filtro.options=Usuarios.get_options()
         
        form.visible = False
        cargar_tabla()

    def eliminar_ui(email):
        Usuarios.eliminar_Usuario(email)
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