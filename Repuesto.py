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
    options = []
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT nombre
        FROM Repuesto
        ORDER BY nombre
    """)
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    for nombre in resultados:
        options.append(ft.dropdown.Option(nombre[0]))
    return options

def obtener_Repuesto_filtrada(nombre):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT nombre, precio_x_unidad, cantidad
        FROM Repuesto
        WHERE nombre LIKE %s
    """, (f"%{nombre}%",))
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    return resultados

def obtener_Repuesto():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT nombre, precio_x_unidad, cantidad
        FROM Repuesto
    """)
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    return resultados

def insertar_repuesto(nombre, precio_x_unidad, cantidad):
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO Repuesto (nombre, precio_x_unidad, cantidad)
            VALUES (%s, %s, %s)
        """, (nombre, precio_x_unidad, cantidad))
        conn.commit()
    except Exception as e:
        print("Error al insertar repuesto:", e)
    finally:
        cursor.close()
        conn.close()

def eliminar_repuesto(nombre):
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Repuesto WHERE nombre = %s", (nombre,))
        conn.commit()
    except Exception as e:
        print("Error al eliminar repuesto:", e)
    finally:
        cursor.close()
        conn.close()

def actualizar_repuesto(nombre, precio_x_unidad, cantidad):
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE Repuesto
            SET precio_x_unidad=%s, cantidad=%s
            WHERE nombre=%s
        """, (precio_x_unidad, cantidad, nombre))
        conn.commit()
    except Exception as e:
        print("Error al actualizar repuesto:", e)
    finally:
        cursor.close()
        conn.close()

def Herramienta_Repuesto(page: ft.Page):
    page.title = "Gestión de Repuesto"
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
        options=get_options(),
    )

    def cargar_tabla(repuestos=None):
        tabla.controls.clear()
        datos = repuestos if repuestos is not None else obtener_Repuesto()
        for c in datos:
            fila = ft.Row([
                ft.Text(str(c[0])),
                ft.Text(str(c[1])),
                ft.Text(str(c[2])),
                ft.IconButton(ft.Icons.EDIT, on_click=lambda e, c=c: mostrar_formulario(c)),
                ft.IconButton(ft.Icons.DELETE, on_click=lambda e, nombre=c[0]: eliminar_ui(nombre)),
            ])
            tabla.controls.append(fila)
        page.update()

    def filtrar_tabla(e):
        print(filtro.value)
        if filtro.value:
            datos = obtener_Repuesto_filtrada(filtro.value)
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
        if modo_edicion.value == "editar":
            actualizar_repuesto(nombre.value, precio_x_unidad.value, cantidad.value)
        else:
            insertar_repuesto(nombre.value, precio_x_unidad.value, cantidad.value)
        form.visible = False
        cargar_tabla()

    def eliminar_ui(nombre_repuesto):
        eliminar_repuesto(nombre_repuesto)
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
