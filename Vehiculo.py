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
            cursor.execute("SELECT matricula FROM Vehiculo ORDER BY matricula")
            resultados = cursor.fetchall()
            return [ft.dropdown.Option(m[0]) for m in resultados]

def obtener_Vehiculo_filtrada(matricula,dni_cliente):
    with conectar_bd() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT *
                FROM Vehiculo
                WHERE matricula LIKE %s,dni_cliente LIKE %s
            """, (f"%{matricula}%",dni_cliente))
            return cursor.fetchall()

def obtener_Vehiculo(dni_cliente):
    with conectar_bd() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM Vehiculo WHERE dni_cliente LIKE %s",(dni_cliente,))
            return cursor.fetchall()

def insertar_Vehiculo(matricula, color, modelo,dni_cliente):
    with conectar_bd() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO Vehiculo
                VALUES (%s, %s, %s, %s)
            """, (matricula, color, modelo, dni_cliente))
            conn.commit()

def eliminar_Vehiculo(matricula):
    with conectar_bd() as conn:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM Vehiculo WHERE matricula = %s", (matricula,))
            conn.commit()

def actualizar_Vehiculo(matricula, color, modelo):
    with conectar_bd() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE Vehiculo
                SET color=%s, modelo=%s
                WHERE matricula=%s
            """, (color, modelo, matricula))
            conn.commit()



def Herramienta_Vehiculo(page: ft.Page,cliente):
    page.title = "Gestión de Vehículos"
    page.scroll = ft.ScrollMode.AUTO

    matricula = ft.TextField(label="Matrícula")
    color = ft.TextField(label="Color")
    modelo = ft.TextField(label="Modelo")
    modo_edicion = ft.Text()

    btn_guardar = ft.ElevatedButton("Guardar")
    btn_cancelar = ft.TextButton("Cancelar")

    form = ft.Column(
        controls=[matricula, color, modelo, ft.Row([btn_guardar, btn_cancelar])],
        visible=False
    )

    tabla = ft.Column()

    filtro = ft.Dropdown(
        border=ft.InputBorder.UNDERLINE,
        editable=True,
        label="Filtro por matrícula",
        options=get_options(),
    )

    def actualizar_opciones():
        filtro.options = get_options()
        page.update()

    def cargar_tabla(vehiculos=None):
        datos = vehiculos
        if vehiculos is None:
            datos = obtener_Vehiculo(cliente[1])
        tabla.controls.clear()
        for c in datos:
            tabla.controls.append(ft.Row([
                ft.Text(str(c[0])),  
                ft.Text(str(c[1])),  
                ft.Text(str(c[2])), 
                ft.Row([
                    ft.IconButton(ft.Icons.EDIT, on_click=lambda e, c=c: mostrar_formulario(c)),
                    ft.IconButton(ft.Icons.DELETE, on_click=lambda e, matricula=c[0]: eliminar_ui(matricula)),
                ]),
            ]))
        page.update()

    def filtrar_tabla(e):
        if filtro.value:
            datos = obtener_Vehiculo_filtrada(filtro.value,cliente[1])
            filtro.value = ""
            cargar_tabla(datos)
        else:
            cargar_tabla()

    def mostrar_formulario(vehiculo=None):
        form.visible = True
        if vehiculo:
            matricula.value = vehiculo[0]
            color.value = vehiculo[1]
            modelo.value = vehiculo[2]
            matricula.disabled = True
            modo_edicion.value = "editar"
        else:
            matricula.value = color.value = modelo.value = ""
            modo_edicion.value = ""
            matricula.disabled = False
        page.update()

    def enviar_datos(e):
        if not matricula.value:
            page.update()
            return

        if modo_edicion.value == "editar":
            actualizar_Vehiculo(matricula.value, color.value, modelo.value)
        else:
            print(cliente)
            insertar_Vehiculo(matricula.value, color.value, modelo.value,cliente[1])

        actualizar_opciones()
        form.visible = False
        cargar_tabla()

    def eliminar_ui(matricula_Vehiculo):
        eliminar_Vehiculo(matricula_Vehiculo)
        actualizar_opciones()
        cargar_tabla()

    def cancelar(e):
        form.visible = False
        page.update()

    btn_guardar.on_click = enviar_datos
    btn_cancelar.on_click = cancelar

    lupa = ft.IconButton(tooltip="Filtrar", icon=ft.Icons.SEARCH, on_click=filtrar_tabla)
    cargar_tabla()

    return ft.Column([
            ft.Text("Vehículos", size=24, weight="bold"),
            ft.ElevatedButton("Agregar Vehículo", on_click=lambda e: mostrar_formulario()),
            form,
            ft.Divider(),
            ft.Row([filtro, lupa]),
            tabla
        ]
    )


if __name__ == "__main__":
    ft.app(target=Herramienta_Vehiculo)
