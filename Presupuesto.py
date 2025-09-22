import flet as ft
import mysql.connector
from classes import Presupuestos

def Herramienta_Presupuesto(page: ft.Page):

    
    page.title = "Gestion de Presupuesto"
    page.scroll = ft.ScrollMode.AUTO

    matricula = ft.TextField(label="Matrícula")
    repuesto = ft.TextField(label="repuesto")
    cantidad = ft.TextField(label="Cantidad")
    legajo = ft.Dropdown(
        border=ft.InputBorder.UNDERLINE,
        editable=True,
        label="legajo",
        options=Presupuestos.get_options_legajos(),
    )

    btn_guardar = ft.ElevatedButton("Guardar")
    btn_cancelar = ft.TextButton("Cancelar")

    form = ft.Column(
        controls=[matricula, repuesto, cantidad, ft.Row([btn_guardar, btn_cancelar])],
        visible=False
    )

    def mostrar_formulario(C=None):
        form.visible = True
        matricula.value = repuesto.value = cantidad.value = legajo.value = ""

        page.update()

    def enviar_datos(e):

        Presupuestos.insertar_Ficha_Tecnica(matricula.value, repuesto.value, cantidad.value, legajo.value)
        
        form.visible = False
        page.update()


    def cancelar(e):
        form.visible = False
        page.update()

    btn_guardar.on_click = enviar_datos
    btn_cancelar.on_click = cancelar

    
    
    page.add(
        ft.Text("Ficha_Tecnica", size=24, weight="bold"),
        ft.ElevatedButton("Agregar Ficha_Tecnica", on_click=lambda e: mostrar_formulario()),
        form,
        ft.Divider())



if __name__ == "__Herramienta_Presupuesto__":
    ft.app(target=Herramienta_Presupuesto)
