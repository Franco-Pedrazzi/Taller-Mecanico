import flet as ft
import mysql.connector

def conectar_bd():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="TallerMecanico"
    )

def get_options_legajos():
    with conectar_bd() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT legajo FROM Empleado ORDER BY legajo")
            resultados = cursor.fetchall()
            return [ft.dropdown.Option(nombre[0]) for nombre in resultados]


def insertar_Ficha_Tecnica(matricula, repuesto, cantidad,legajos):
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        cursor.execute("""
                SELECT id_
                FROM Reparaciones
                WHERE matricula LIKE %s
            """, (repuesto,))
        id_reparacion=cursor.fetchone()
        if not id_reparacion:
            cursor.execute("INSERT INTO Reparaciones (matricula_vehiculo) VALUES (%s)",
                       (matricula,))
        
        cursor.execute("""
                SELECT precio_x_unidad
                FROM Repuesto
                WHERE nombre LIKE %s
            """, (repuesto,))
        precio=cursor.fetchone()

        precio*=cantidad

        cursor.execute("""
                SELECT precio_x_unidad
                FROM Repuesto
                WHERE nombre LIKE %s
            """, (f"%{repuesto}%",))
        id_reparacion=cursor.fetchone()

        cursor.execute("INSERT INTO Repuesto_Reparacion (repuesto,cantidad,Precio,reparacion_id) VALUES (%s,%s,%s,%s)",
                       (repuesto,cantidad,precio,id_reparacion))
        conn.commit()
    except Exception as e:
        print("Error al insertar Ficha_Tecnica:", e)
    finally:
        cursor.close()
        conn.close()


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
        options=get_options_legajos(),
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

        insertar_Ficha_Tecnica(matricula.value, repuesto.value, cantidad.value, legajo.value)
        
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
