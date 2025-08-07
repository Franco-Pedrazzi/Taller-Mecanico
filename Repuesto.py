import flet as ft
import mysql.connector

def conectar_bd():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="TallerMecanico"
    )

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

def insertar_repuesto(nombre , precio_x_unidad, cantidad):
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Repuesto (nombre, precio_x_unidad, cantidad) VALUES (%s,%s,%s)",
                       (nombre, precio_x_unidad, cantidad))
        conn.commit()
    except Exception as e:
        print("Error al insertar repuesto:", e)
    finally:
        cursor.close()
        conn.close()

def eliminar_repuesto(e,nombre):
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
            UPDATE Repuesto SET precio_x_unidad=%s, cantidad=%s WHERE nombre=%s
        """, (precio_x_unidad,cantidad, nombre))
        conn.commit()
    except Exception as e:
        print("Error al actualizar repuesto:", e)
    finally:
        cursor.close()
        conn.close()

def Herramienta_Repuesto(page: ft.Page):
    page.title = "Gestion de Repuesto"
    page.scroll = ft.ScrollMode.AUTO
    
    nombre = ft.TextField(label="Nombre")
    precio_x_unidad = ft.TextField(label="precio_x_unidad")
    cantidad = ft.TextField(label="cantida")
    modo_edicion = ft.Text() 

    btn_guardar = ft.ElevatedButton("Guardar")
    btn_cancelar = ft.TextButton("Cancelar")

    form = ft.Column(
        controls=[nombre, precio_x_unidad, cantidad, ft.Row([btn_guardar, btn_cancelar])],
        visible=False
    )
    tabla = ft.Column()

    def cargar_tabla():
        tabla.controls.clear()
        Repuesto = obtener_Repuesto()
        for c in Repuesto:
            fila = ft.Row([
                ft.Text(c[0]),  
                ft.Text(c[1]),  
                ft.Text(c[2]),   

                ft.IconButton(ft.Icons.EDIT, on_click=lambda e, c=c: mostrar_formulario(e, c)),
                ft.IconButton(ft.Icons.DELETE, on_click=lambda e, nombre=c[0]: eliminar_ui(e, nombre)),
            ])
            tabla.controls.append(fila)
        page.update()

    def mostrar_formulario(e=None, repuesto=None):
        form.visible = True
        if repuesto:
            nombre.value = repuesto[0]
            precio_x_unidad.value = repuesto[1]
            cantidad.value = repuesto[2]
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
        page.update()

    def eliminar_ui(e, nombre):
        eliminar_repuesto(e, nombre)
        cargar_tabla()

    def cancelar(e):
        form.visible = False
        page.update()

    btn_guardar.on_click = enviar_datos
    btn_cancelar.on_click = cancelar

    page.add(
        ft.Text("Repuesto", size=24, weight="bold"),
        ft.ElevatedButton("Agregar repuesto", on_click=mostrar_formulario),
        form,
        ft.Divider(),
        tabla
    )

    cargar_tabla()

if __name__ == "__Herramienta_Repuesto__":
    ft.app(target=Herramienta_Repuesto)
