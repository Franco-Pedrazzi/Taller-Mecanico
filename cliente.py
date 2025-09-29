import flet as ft
import mysql.connector
from Vehiculo import Herramienta_Vehiculo
from classes import cliente,Persona

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
        options=cliente.get_options(),
    )


    def cargar_tabla(Cliente=None):
        datos = Cliente
        if Cliente is None:
            datos= cliente.obtener_Cliente()
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
            if len(Row.controls)==2:
                Row.controls.pop(-1)
            page.update()
            for row in tabla.controls:
                checkbox = row.controls[0]
                checkbox.disabled = False
        tabla.update()
        
    def filtrar_tabla(e):
        if len(Row.controls)==2:
            Row.controls.pop(-1)
        if filtro.value:
            datos = cliente.obtener_Cliente_filtrada(filtro.value)
            filtro.value = ""
            cargar_tabla(datos)
        else:
            cargar_tabla()

    def actualizar_opciones():
        filtro.options = cliente.get_options()
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
            Persona.actualizar_Personas(dni.value, nombre.value, apellido.value, telefono.value, direccion.value)
        else:
            nuevo=cliente(dni.value, nombre.value, apellido.value, telefono.value, direccion.value)
        
        if len(Row.controls)==2:
            Row.controls.pop(-1)
        
        form.visible = False
        filtro.options = cliente.get_options()
        cargar_tabla()
        page.update()

    def eliminar_ui(c):
        Persona.eliminar_Personas(c[1])
        actualizar_opciones()
        if len(Row.controls)==2:
            Row.controls.pop(-1)
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
