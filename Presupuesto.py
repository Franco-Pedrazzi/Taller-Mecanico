import flet as ft
from classes import Presupuestos, Empleados, Vehiculos, Repuestos,FichaTecnica

def Herramienta_Presupuesto(page: ft.Page):
    id = ft.Text(value="")
    id_aux=ft.Text(value="")

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
    resultado = ft.Text(value="0", size=20, visible=False)

    def mostrar_formulario(C=None):
        form.visible = True
        if isinstance(C, (list, tuple)):
            id_aux.value=C[0]
            matricula.value = C[1]
            repuesto.value = C[2]
            cantidad.value = C[4]
            legajo.value = C[1]
            matricula.disabled = True
            modo_edicion.value = "editar"
        else:
            id_aux.value = repuesto.value = cantidad.value = legajo.value = ""
            if matricula.value==False:
                matricula.disabled = True
            modo_edicion.value = ""
        page.update()

    def enviar_datos(c):
        if modo_edicion.value=="":
            repuesto_datos = Repuestos.obtener_Repuesto_filtrada(repuesto.value)[0]
            total = float(repuesto_datos[1]) * float(cantidad.value)
            resultado.visible = True
            final.visible = True
            form.visible = False
            
            if id.value == "":
                id.value = Presupuestos.insertar_Presupuestos(matricula.value, repuesto.value, float(cantidad.value), legajo.value, total)
            else:
                Presupuestos.insertar_Presupuestos(matricula.value, repuesto.value, float(cantidad.value), legajo.value, total, id.value)
        else:
            repuesto_datos = Repuestos.obtener_Repuesto_filtrada(repuesto.value)[0]
            total = float(repuesto_datos[1]) * float(cantidad.value)
            Presupuestos.actualizar_Presupuesto(repuesto.value, cantidad.value, legajo.value,total , id_aux.value)
            form.visible = False

        cargar_tabla()
        page.update()

    def cancelar(e):
        form.visible = False
        page.update()

    def terminar_proceso(e):
        final.visible = False
        nroEmpleados = []
        for fila in tabla.controls[2:]: 
            nroEmpleados.append(fila.controls[3].value)
        nroEmpleados=len(set(nroEmpleados))
        CistoMano=nroEmpleados*1000
        datos = Presupuestos.obtener_Presupuesto(id.value)
        reparacion = datos[0]
        FichaTecnica.insertar_FichaTecnica(reparacion[2],nroEmpleados,resultado.value,CistoMano,float(resultado.value)+CistoMano)
        resultado.value = "Presupuesto confirmado con exito"
        matricula.value = repuesto.value = cantidad.value = legajo.value = ""
        page.update()

    def borrar(e):
        Presupuestos.eliminar_Presupuesto(id.value)
        id.value = ""
        matricula.value=""
        tabla.controls.clear()
        resultado.value = "Presupuesto eliminado"
        final.visible = False
        page.update()

    def eliminar_ui(c):
        print(c[0])
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
                ft.Text(f"Matricula: {reparacion[2]}"),
                ft.Text(f"Fecha: {reparacion[1]}"),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        )
        tabla.controls.append(
                ft.Row([
                    ft.Text("id"),
                    ft.Text("repuesto"),  
                    ft.Text("legajo"),  
                    ft.Text("precio")
                ]))
            
        for c in detalles:
            tabla.controls.append(
                ft.Row([
                    ft.Text(str(c[1])),
                    ft.Text(str(c[2])),  
                    ft.Text(str(c[4])),  
                    ft.Text(str(c[5])),  
                    ft.Row([
                        ft.IconButton(ft.Icons.EDIT, on_click=lambda e, c=c: mostrar_formulario(c)),
                        ft.IconButton(ft.Icons.DELETE, on_click=lambda e, c=c: eliminar_ui(c)),
                    ]),
                ])
            )

        total_actual = float(0)
        for fila in tabla.controls[2:]: 
            total_actual += float(fila.controls[3].value)
        resultado.value = str(total_actual)

        page.update()

    btn_guardar.on_click = enviar_datos
    btn_cancelar.on_click = cancelar
    btn_confirmar.on_click = terminar_proceso
    btn_borrar.on_click = borrar
    btn_agregar.on_click = mostrar_formulario

    page.add(
        ft.Text("Presupuestos", size=24, weight="bold"),
        btn_agregar,
        form,
        ft.Divider(),
        resultado,
        tabla,
        final,
    )
