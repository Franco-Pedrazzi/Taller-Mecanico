import flet as ft
import mysql.connector

def conectar_bd():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="TallerMecanico"
    )

def obtener_empleado():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.legajo, p.dni, p.nombre, p.apellido, p.tel, p.dir
        FROM Empleado c
        JOIN Persona p ON c.dni_empleado = p.dni
    """)
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    return resultados

def insertar_empleado(legajo, dni, nombre, apellido, tel, dir_):
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Persona (dni, nombre, apellido, tel, dir) VALUES (%s, %s, %s, %s, %s)",
                       (dni, nombre, apellido, tel, dir_))
        cursor.execute("INSERT INTO empleado (legajo, dni_empleado) VALUES (%s, %s)",
                       (legajo, dni))
        conn.commit()
    except Exception as e:
        print("Error al insertar empleado:", e)
    finally:
        cursor.close()
        conn.close()

def eliminar_empleado(dni_empleado):
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM empleado WHERE dni_empleado = %s", (dni_empleado,))
        cursor.execute("DELETE FROM Persona WHERE dni = %s", (dni_empleado,))
        conn.commit()
    except Exception as e:
        print("Error al eliminar empleado:", e)
    finally:
        cursor.close()
        conn.close()

def actualizar_empleado(legajo, dni, nombre, apellido, tel, dir_):
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE Persona SET nombre=%s, apellido=%s, tel=%s, dir=%s WHERE dni=%s
        """, (nombre, apellido, tel, dir_, dni))
        cursor.execute("""
            UPDATE empleado SET legajo=%s WHERE dni_empleado=%s
        """, (legajo, dni))
        conn.commit()
    except Exception as e:
        print("Error al actualizar empleado:", e)
    finally:
        cursor.close()
        conn.close()

def Herramienta_empleado(page: ft.Page):
    page.title = "Gestión de empleado"
    page.scroll = ft.ScrollMode.AUTO

    nombre = ft.TextField(label="Nombre")
    apellido = ft.TextField(label="Apellido")
    dni = ft.TextField(label="DNI")
    telefono = ft.TextField(label="Teléfono")
    direccion = ft.TextField(label="Dirección")
    legajo = ft.TextField(label="legajo empleado")
    modo_edicion = ft.Text()  

    btn_guardar = ft.ElevatedButton("Guardar")
    btn_cancelar = ft.TextButton("Cancelar")

    form = ft.Column(
        controls=[legajo, dni, nombre, apellido, telefono, direccion, ft.Row([btn_guardar, btn_cancelar])],
        visible=False
    )
    tabla = ft.Column()

    def cargar_tabla():
        tabla.controls.clear()
        empleado = obtener_empleado()
        for c in empleado:
            fila = ft.Row([
                ft.Text(c[0]),  
                ft.Text(c[1]),  
                ft.Text(c[2]),  
                ft.Text(c[3]),  
                ft.Text(c[4]),  
                ft.Text(c[5]),  
                ft.IconButton(ft.Icons.EDIT, on_click=lambda e, c=c: mostrar_formulario(e, c)),
                ft.IconButton(ft.Icons.DELETE, on_click=lambda e, dni=c[1]: eliminar_ui(e, dni)),
            ])
            tabla.controls.append(fila)
        page.update()

    def mostrar_formulario(e=None, empleado=None):
        form.visible = True
        if empleado:
            legajo.value = empleado[0]
            dni.value = empleado[1]
            nombre.value = empleado[2]
            apellido.value = empleado[3]
            telefono.value = empleado[4]
            direccion.value = empleado[5]
            legajo.disabled = True
            dni.disabled = True
            modo_edicion.value = "editar"
        else:
            legajo.value = dni.value = nombre.value = apellido.value = telefono.value = direccion.value = ""
            legajo.disabled = False
            dni.disabled = False
            modo_edicion.value = ""
        page.update()

    def enviar_datos(e):
        if modo_edicion.value == "editar":
            actualizar_empleado(legajo.value, dni.value, nombre.value, apellido.value, telefono.value, direccion.value)
        else:
            insertar_empleado(legajo.value, dni.value, nombre.value, apellido.value, telefono.value, direccion.value)
        form.visible = False
        cargar_tabla()
        page.update()

    def eliminar_ui(e, dni_empleado):
        eliminar_empleado(dni_empleado)
        cargar_tabla()

    def cancelar(e):
        form.visible = False
        page.update()

    btn_guardar.on_click = enviar_datos
    btn_cancelar.on_click = cancelar

    page.add(
        ft.Text("empleado", size=24, weight="bold"),
        ft.ElevatedButton("Agregar empleado", on_click=mostrar_formulario),
        form,
        ft.Divider(),
        tabla
    )

    cargar_tabla()

if __name__ == "__Herramienta_empleado__":
    ft.app(target=Herramienta_empleado)
