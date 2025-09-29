import flet as ft
from classes import Presupuestos, Empleados, Vehiculos, Repuestos

def Herramienta_Presupuesto(page: ft.Page):
    id = ft.Text(value="")
    page.title = "Gestión de Presupuesto"
    page.scroll = ft.ScrollMode.AUTO

    matricula = ft.Dropdown(
        border=ft.InputBorder.UNDERLINE,
        editable=True,
        label="Matrícula",
        options=Vehiculos.get_options(),
    )
    repuesto = ft.Dropdown(
        border=ft.InputBorder.UNDERLINE,
        editable=True,
        label="Repuesto",
        options=Repuestos.get_options(),
    )
    cantidad = ft.TextField(label="Cantidad")
    legajo = ft.Dropdown(
        border=ft.InputBorder.UNDERLINE,
        editable=True,
        label="Legajo",
        options=Empleados.get_options(),
    )

    tabla = ft.Column()
    modo_edicion = ft.Text()

    btn_guardar = ft.ElevatedButton("Guardar")
    btn_cancelar = ft.TextButton("Cancelar")
    btn_confirmar = ft.ElevatedButton("Confirmar Presupuesto")
    btn_borrar = ft.TextButton("Borrar Todo")
    btn_agregar = ft.ElevatedButton("Agregar Repuesto")

    form = ft.Column(
        controls=[matricula, repuesto, cantidad, legajo, ft.Row([btn_guardar, btn_cancelar])],
        visible=False,
    )

    final = ft.Row([btn_borrar, btn_confirmar], visible=False)
    resultado = ft.Text(value="", size=20)

    def mostrar_formulario(C=None):
        form.visible = True
        if isinstance(C, (list, tuple)):
            matricula.value = C[1]
            repuesto.value = C[2]
            cantidad.value = str(C[3])
            legajo.value = C[4]
            matricula.disabled = True
            modo_edicion.value = "editar"
        else:
            matricula.value = repuesto.value = cantidad.value = legajo.value = ""
            matricula.disabled = False
            modo_edicion.value = ""
        page.update()

    def enviar_datos(e):
        if modo_edicion.value==False:
            repuesto_datos = Repuestos.obtener_Repuesto_filtrada(repuesto.value)[0]
            total = float(repuesto_datos[1]) * float(cantidad.value)
            resultado.value = f"Subtotal: ${total:.2f}"
            final.visible = True
            form.visible = False

            if id.value == "":
                id.value = Presupuestos.insertar_Presupuestos(matricula.value, repuesto.value, float(cantidad.value), legajo.value, total)
            else:
                Presupuestos.insertar_Presupuestos(matricula.value, repuesto.value, float(cantidad.value), legajo.value, total, id.value)
        else:
            pass
        cargar_tabla()
        page.update()

    def cancelar(e):
        form.visible = False
        page.update()

    def terminar_proceso(e):
        final.visible = False
        matricula.value = repuesto.value = cantidad.value = legajo.value = ""
        resultado.value = "Presupuesto confirmado con exito"
        page.update()

    def borrar(e):
        Presupuestos.eliminar_Presupuesto(id.value)
        id.value = ""
        tabla.controls.clear()
        resultado.value = "Presupuesto eliminado"
        final.visible = False
        page.update()

    def eliminar_ui(c):
        Presupuestos.eliminar_Presupuesto(c[0])  
        cargar_tabla()

    def cargar_tabla():
        tabla.controls.clear()
        if id.value == "":
            page.update()
            return

        datos = Presupuestos.obtener_Presupuesto(id.value)
        reparacion = datos[0]
        detalles = datos[1]

        tabla.controls.append(
            ft.Row([
                ft.Text(f"Reparación #{reparacion[0]}"),
                ft.Text(f"Matrícula: {reparacion[1]}"),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        )

        for c in detalles:
            tabla.controls.append(
                ft.Row([
                    ft.Text(str(c[2])),  
                    ft.Text(str(c[3])),  
                    ft.Text(str(c[4])),  
                    ft.Row([
                        ft.IconButton(ft.Icons.EDIT, on_click=lambda e, c=c: mostrar_formulario(c)),
                        ft.IconButton(ft.Icons.DELETE, on_click=lambda e, c=c: eliminar_ui(c)),
                    ]),
                ])
            )
        page.update()

    btn_guardar.on_click = enviar_datos
    btn_cancelar.on_click = cancelar
    btn_confirmar.on_click = terminar_proceso
    btn_borrar.on_click = borrar
    btn_agregar.on_click = mostrar_formulario

    page.add(
        ft.Text("Ficha Técnica", size=24, weight="bold"),
        btn_agregar,
        form,
        ft.Divider(),
        resultado,
        tabla,
        final,
    )
