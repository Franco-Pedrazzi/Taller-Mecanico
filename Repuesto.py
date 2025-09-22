import flet as ft
import mysql.connector
from classes import Repuestos


def Herramienta_Repuesto(page: ft.Page):
    page.title = "Gestion de Repuestos"
    page.scroll = ft.ScrollMode.AUTO

    nombre = ft.TextField(label="Nombre")
    precio_x_unidad = ft.TextField(label="Precio por unidad")
    cantidad = ft.TextField(label="Cantidad")
    modo_edicion = ft.Text()

    btn_guardar = ft.ElevatedButton("Guardar")
    btn_cancelar = ft.TextButton("Cancelar")

    form = ft.Column(
        controls=[nombre, precio_x_unidad, cantidad, ft.Row([btn_guardar, btn_cancelar])],
        visible=False
    )

    tabla = ft.Column()

    filtro = ft.Dropdown(
        border=ft.InputBorder.UNDERLINE,
        editable=True,
        label="Filtro",
        options=Repuestos.get_options(),
    )

    def actualizar_opciones():
        filtro.options = Repuestos.get_options()
        page.update()

    def cargar_tabla(Repuesto=None):
        datos = Repuesto
        if Repuesto is None:
            datos= Repuestos.obtener_Repuesto()
        tabla.controls.clear()
        for c in datos:
                tabla.controls.append(ft.Row([
                        ft.Text(str(c[0])),
                        ft.Text(str(c[1])),
                        ft.Text(str(c[2])),
                        
                        ft.Row([
                                ft.IconButton(ft.Icons.EDIT, on_click=lambda e, c=c: mostrar_formulario(c)),
                                ft.IconButton(ft.Icons.DELETE, on_click=lambda e, nombre=c[0]: eliminar_ui(nombre)),
                            ]),
                    
                ])
            )
        page.update()

    def filtrar_tabla(e):
        if filtro.value:
            datos = Repuestos.obtener_Repuesto_filtrada(filtro.value)
            filtro.value = ""
            cargar_tabla(datos)
        else:
            cargar_tabla()

    def mostrar_formulario(repuesto=None):
        form.visible = True
        if repuesto:
            nombre.value = repuesto[0]
            precio_x_unidad.value = str(repuesto[1])
            cantidad.value = str(repuesto[2])
            nombre.disabled = True
            modo_edicion.value = "editar"
        else:
            nombre.value = precio_x_unidad.value = cantidad.value = ""
            modo_edicion.value = ""
            nombre.disabled = False
        page.update()

    def enviar_datos(e):
        if not nombre.value:
            page.update()
            return

        try:
            precio = float(precio_x_unidad.value)
            cantidad_int = int(cantidad.value)

        except ValueError:
            page.update()
            return

        if modo_edicion.value == "editar":
            Repuestos.actualizar_repuesto(nombre.value, precio, cantidad_int)
        else:
            Repuestos.insertar_repuesto(nombre.value, precio, cantidad_int)
        filtro.options=Repuestos.get_options()
         
        form.visible = False
        cargar_tabla()

    def eliminar_ui(nombre_repuesto):
        Repuestos.eliminar_repuesto(nombre_repuesto)
        actualizar_opciones()
        cargar_tabla()

    def cancelar(e):
        form.visible = False
        page.update()

    btn_guardar.on_click = enviar_datos
    btn_cancelar.on_click = cancelar

    lupa = ft.IconButton(tooltip="Filtrar", icon=ft.Icons.SEARCH, on_click=filtrar_tabla)

    page.add(
        ft.Text("Repuestos", size=24, weight="bold"),
        ft.ElevatedButton("Agregar repuesto", on_click=lambda e: mostrar_formulario()),
        form,
        ft.Divider(),
        ft.Row([filtro, lupa]),
        tabla
    )

    cargar_tabla()


if __name__ == "__main__":
    ft.app(target=Herramienta_Repuesto)