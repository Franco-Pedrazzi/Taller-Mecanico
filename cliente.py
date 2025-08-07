import flet as ft
import mysql.connector

def conectar_bd():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="TallerMecanico"
    )

def obtener_clientes():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.cod_cliente, p.dni, p.nombre, p.apellido, p.tel, p.dir
        FROM Cliente c
        JOIN Persona p ON c.dni_cliente = p.dni
    """)
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    return resultados

def insertar_cliente(cod_cliente, dni, nombre, apellido, tel, dir_):
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Persona (dni, nombre, apellido, tel, dir) VALUES (%s, %s, %s, %s, %s)",
                       (dni, nombre, apellido, tel, dir_))
        cursor.execute("INSERT INTO Cliente (cod_cliente, dni_cliente) VALUES (%s, %s)",
                       (cod_cliente, dni))
        conn.commit()
    except Exception as e:
        print("Error al insertar cliente:", e)
    finally:
        cursor.close()
        conn.close()

def eliminar_cliente(dni_cliente):
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Cliente WHERE dni_cliente = %s", (dni_cliente,))
        cursor.execute("DELETE FROM Persona WHERE dni = %s", (dni_cliente,))
        conn.commit()
    except Exception as e:
        print("Error al eliminar cliente:", e)
    finally:
        cursor.close()
        conn.close()

def actualizar_cliente(cod_cliente, dni, nombre, apellido, tel, dir_):
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE Persona SET nombre=%s, apellido=%s, tel=%s, dir=%s WHERE dni=%s
        """, (nombre, apellido, tel, dir_, dni))
        cursor.execute("""
            UPDATE Cliente SET cod_cliente=%s WHERE dni_cliente=%s
        """, (cod_cliente, dni))
        conn.commit()
    except Exception as e:
        print("Error al actualizar cliente:", e)
    finally:
        cursor.close()
        conn.close()

def Herramienta_Cliente(page: ft.Page):
    page.title = "Gestión de Clientes"
    page.scroll = ft.ScrollMode.AUTO

    nombre = ft.TextField(label="Nombre")
    apellido = ft.TextField(label="Apellido")
    dni = ft.TextField(label="DNI")
    telefono = ft.TextField(label="Teléfono")
    direccion = ft.TextField(label="Dirección")
    codigo = ft.TextField(label="Código Cliente")
    modo_edicion = ft.Text()  

    btn_guardar = ft.ElevatedButton("Guardar")
    btn_cancelar = ft.TextButton("Cancelar")

    form = ft.Column(
        controls=[codigo, dni, nombre, apellido, telefono, direccion, ft.Row([btn_guardar, btn_cancelar])],
        visible=False
    )
    tabla = ft.Column()

    def cargar_tabla():
        tabla.controls.clear()
        clientes = obtener_clientes()
        for c in clientes:
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

    def mostrar_formulario(e=None, cliente=None):
        form.visible = True
        if cliente:
            codigo.value = cliente[0]
            dni.value = cliente[1]
            nombre.value = cliente[2]
            apellido.value = cliente[3]
            telefono.value = cliente[4]
            direccion.value = cliente[5]
            codigo.disabled = True
            dni.disabled = True
            modo_edicion.value = "editar"
        else:
            codigo.value = dni.value = nombre.value = apellido.value = telefono.value = direccion.value = ""
            codigo.disabled = False
            dni.disabled = False
            modo_edicion.value = ""
        page.update()

    def enviar_datos(e):
        if modo_edicion.value == "editar":
            actualizar_cliente(codigo.value, dni.value, nombre.value, apellido.value, telefono.value, direccion.value)
        else:
            insertar_cliente(codigo.value, dni.value, nombre.value, apellido.value, telefono.value, direccion.value)
        form.visible = False
        cargar_tabla()
        page.update()

    def eliminar_ui(e, dni_cliente):
        eliminar_cliente(dni_cliente)
        cargar_tabla()

    def cancelar(e):
        form.visible = False
        page.update()

    btn_guardar.on_click = enviar_datos
    btn_cancelar.on_click = cancelar

    page.add(
        ft.Text("Clientes", size=24, weight="bold"),
        ft.ElevatedButton("Agregar Cliente", on_click=mostrar_formulario),
        form,
        ft.Divider(),
        tabla
    )

    cargar_tabla()

if __name__ == "__Herramienta_Cliente__":
    ft.app(target=Herramienta_Cliente)
