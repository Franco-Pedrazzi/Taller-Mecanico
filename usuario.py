import flet as ft
import mysql.connector

def conectar_bd():
    return mysql.connector.connect(
        host='localhost',
        port='3306',
        user='root',
        password='123456',
        database='TallerMecanico',
        ssl_disabled=True
    )

def obtener_usuarios():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT id_usuario, nombre, email FROM Usuarios")
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    return resultados

def insertar_usuario(nombre, email):
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Usuarios (nombre, email) VALUES (%s, %s)", (nombre, email))
        conn.commit()
    except mysql.connector.Error as e:
        print("Error al insertar usuario:", e)
        raise
    finally:
        cursor.close()
        conn.close()

def actualizar_usuario(id_usuario, nombre, email):
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE Usuarios SET nombre=%s, email=%s WHERE id_usuario=%s",
                       (nombre, email, id_usuario))
        conn.commit()
    except mysql.connector.Error as e:
        print("Error al actualizar usuario:", e)
        raise
    finally:
        cursor.close()
        conn.close()

def eliminar_usuario(id_usuario):
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Usuarios WHERE id_usuario=%s", (id_usuario,))
        conn.commit()
    except mysql.connector.Error as e:
        print("Error al eliminar usuario:", e)
        raise
    finally:
        cursor.close()
        conn.close()

def Herramienta_Usuario(page: ft.Page, main_menu=None):
    page.title = "Gestión de Usuarios"
    page.scroll = ft.ScrollMode.AUTO

    id_field = ft.TextField(label="ID", disabled=True)
    nombre = ft.TextField(label="Nombre")
    email = ft.TextField(label="Email")
    modo_edicion = ft.Text()  

    btn_guardar = ft.ElevatedButton("Guardar")
    btn_cancelar = ft.TextButton("Cancelar")

    form = ft.Column(
        controls=[id_field, nombre, email, ft.Row([btn_guardar, btn_cancelar])],
        visible=False
    )
    tabla = ft.Column()

    def show_message(msg):
        page.snack_bar = ft.SnackBar(ft.Text(msg))
        page.snack_bar.open = True
        page.update()

    def cargar_tabla():
        tabla.controls.clear()
        try:
            usuarios = obtener_usuarios()
            for u in usuarios:
                fila = ft.Row([
                    ft.Text(str(u[0])),
                    ft.Text(u[1]),
                    ft.Text(u[2]),
                    ft.IconButton(ft.Icons.EDIT, on_click=lambda e, u=u: mostrar_formulario(e, u)),
                    ft.IconButton(ft.Icons.DELETE, on_click=lambda e, idu=u[0]: eliminar_ui(e, idu)),
                ])
                tabla.controls.append(fila)
        except Exception as e:
            print("Error cargando usuarios:", e)
            show_message("Error al cargar usuarios. Ver consola.")
        page.update()

    def mostrar_formulario(e=None, usuario=None):
        form.visible = True
        if usuario:
            id_field.value = str(usuario[0])
            nombre.value = usuario[1]
            email.value = usuario[2]
            id_field.disabled = True
            modo_edicion.value = "editar"
        else:
            id_field.value = ""
            nombre.value = ""
            email.value = ""
            id_field.disabled = True
            modo_edicion.value = ""
        page.update()

    def enviar_datos(e):
        if not nombre.value or not email.value:
            show_message("Completá todos los campos.")
            return

        if modo_edicion.value == "editar":
            try:
                actualizar_usuario(int(id_field.value), nombre.value, email.value)
                show_message("Usuario actualizado.")
            except Exception as ex:
                print("Error al actualizar:", ex)
                show_message("Error al actualizar. Ver consola.")
        else:
            try:
                insertar_usuario(nombre.value, email.value)
                show_message("Usuario insertado.")
            except Exception as ex:
                print("Error al insertar:", ex)
                show_message("Error al insertar. Ver consola.")

        form.visible = False
        cargar_tabla()
        page.update()

    def eliminar_ui(e, id_usuario):
        try:
            eliminar_usuario(id_usuario)
            show_message("Usuario eliminado.")
        except Exception as ex:
            print("Error al eliminar:", ex)
            show_message("No se pudo eliminar el usuario. Ver consola.")
        cargar_tabla()

    def cancelar(e):
        form.visible = False
        page.update()

    btn_guardar.on_click = enviar_datos
    btn_cancelar.on_click = cancelar

    page.add(
        ft.Text("Usuarios", size=24, weight="bold"),
        ft.ElevatedButton("Agregar Usuario", on_click=lambda e: mostrar_formulario(e, None)),
        form,
        ft.Divider(),
        tabla
    )

    cargar_tabla()

if __name__ == "__main__":
    ft.app(target=Herramienta_Usuario)
