import flet as ft
import mysql.connector


from cliente import Herramienta_Cliente
from Empleado import Herramienta_Empleado
from Provedor import Herramienta_Provedor
from Repuesto import Herramienta_Repuesto
from usuario import Herramienta_Usuario
from Ficha_Tecnica import Herramienta_Ficha_Tecnica


def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            port='3306',
            user='root',
            password='123456',
            database='TallerMecanico',
            ssl_disabled=True
        )
        if connection.is_connected():
            print('Conexion exitosa')
            return connection
    except Exception as ex:
        print('Conexion erronea')
        print(ex)
        return None

connection = connect_to_db()




def menu_principal(page: ft.Page,name):
    page.window.maximized=True
    page.title = "Administracion de Taller Mecanico"

    cliente_icono = ft.Image(src="C:/Users/nemer/OneDrive/Desktop/carpetas/trabajos/Tps progra/Flet/Taller-Mecanico/iconos//usuario.png", width=28, height=28)
    cliente_item = ft.Row(
        controls=[
            cliente_icono,
            ft.Text("Cliente"),
        ],
        alignment=ft.MainAxisAlignment.START,
        spacing=8
    )
    
    proveedor_icono = ft.Image(src="C:/Users/nemer/OneDrive/Desktop/carpetas/trabajos/Tps progra/Flet/Taller-Mecanico/iconos//proveedor.png", width=28, height=28)
    proveedor_item = ft.Row(
        controls=[
            proveedor_icono,
            ft.Text("Proveedor"),
        ],
        alignment=ft.MainAxisAlignment.START,
        spacing=8
    )
    
    repuesto_icono = ft.Image(src="C:/Users/nemer/OneDrive/Desktop/carpetas/trabajos/Tps progra/Flet/Taller-Mecanico/iconos//caja-de-cambios.png", width=28, height=28)  
    repuesto_item = ft.Row(
        controls=[
            repuesto_icono,
            ft.Text("Repuesto"),
        ],
        alignment=ft.MainAxisAlignment.START,
        spacing=8
    )
    
    empleado_icono = ft.Image(src="C:/Users/nemer/OneDrive/Desktop/carpetas/trabajos/Tps progra/Flet/Taller-Mecanico/iconos//empleado.png", width=28, height=28)  
    empleado_item = ft.Row(
        controls=[
            empleado_icono,
            ft.Text("Empleado"),
        ],
        alignment=ft.MainAxisAlignment.START,
        spacing=8
    ) 
    
    usuario_icono = ft.Image(src="C:/Users/nemer/OneDrive/Desktop/carpetas/trabajos/Tps progra/Flet/Taller-Mecanico/iconos//usuarios.png", width=28, height=28)  
    usuario_item = ft.Row(
        controls=[
            usuario_icono,
            ft.Text("Usuario"),
        ],
        alignment=ft.MainAxisAlignment.START,
        spacing=8
    )
    
    ficha_tecnica_icono=ft.Image(src="C:/Users/nemer/OneDrive/Desktop/carpetas/trabajos/Tps progra/Flet/Taller-Mecanico/iconos//auto.png", width=28, height=28)
    ficha_tecnica_item=ft.Row(
        controls=[
            ficha_tecnica_icono,
            ft.Text("Ficha Tecnica")
        ],
        alignment=ft.MainAxisAlignment.START,
        spacing=8
    )
    
    presupuesto_icono=ft.Image(src="C:/Users/nemer/OneDrive/Desktop/carpetas/trabajos/Tps progra/Flet/Taller-Mecanico/iconos//presupuesto.png", width=28, height=28)
    presupuesto_icono_item=ft.Row(
         controls=[
             presupuesto_icono,
             ft.Text("Presupuesto")
         ]
     )
    
    archivo_menu = ft.PopupMenuButton(
        items=[
            ft.PopupMenuItem(text="Copiar", icon=ft.Icons.COPY),
            ft.PopupMenuItem(text="Salir", icon=ft.Icons.EXIT_TO_APP),
        ],
        content=ft.Text("Archivo"), tooltip="Archivo"
    )

    herramientas_menu = ft.PopupMenuButton(
        items=[
            ft.PopupMenuItem(content=cliente_item, on_click=lambda e: cliente(e, page,name)),
            ft.PopupMenuItem(content=proveedor_item, on_click=lambda e:proveedor(e, page,name)),
            ft.PopupMenuItem(content=repuesto_item, on_click=lambda e: Repuesto(e, page,name)),
            ft.PopupMenuItem(content=empleado_item, on_click=lambda e: empleado(e, page,name)),
            ft.PopupMenuItem(content=usuario_item, on_click=lambda e: usuario(e, page,name)),
        ],
        content=ft.Text("Herramientas"), tooltip="Administrador de archivos maestros"
        
    )
    
    administracion = ft.PopupMenuButton(
        items=[
            ft.PopupMenuItem(content=ficha_tecnica_item),
            ft.PopupMenuItem(content=presupuesto_icono_item),
        ],
        content=ft.Text("Administracion"), tooltip="Administracion de presupuesto y ficha tecnica"
        
    )

    boton_cliente_item=ft.Row(
        controls=[
            cliente_icono,
        ],
    )
    boton_cliente = ft.IconButton(content=boton_cliente_item, tooltip="Cliente")
    
    
    boton_repuesto_item=ft.Row(
        controls=[
            repuesto_icono,
        ],
    )
    boton_producto = ft.IconButton(content=boton_repuesto_item, tooltip="Repuesto")
    
    boton_ficha_tecnica_item=ft.Row(
        controls=[
                 ficha_tecnica_icono,
        ]
    )
    boton_ficha_tecnica = ft.IconButton(content=boton_ficha_tecnica_item,tooltip="Ficha Tecnica")

    boton_presupuesto_item=ft.Row(
        controls=[
            presupuesto_icono,
        ]
    )
    boton_presupuesto=ft.IconButton(content=boton_presupuesto_item,tooltip="Presupuesto")
    
    
    
    
    page.add(
        ft.Row(
            controls=[
                ft.Text(f"hola {name}     ",size=24, weight="bold"),
                archivo_menu,
                administracion,
                herramientas_menu
                
            ],
            spacing=10,
        ),
        
        ft.Row(
            controls=[
                boton_cliente,
                boton_producto,
                boton_ficha_tecnica,
                boton_presupuesto
            ]
        )
    
    )

def cliente(e, page: ft.Page,name):
    page.controls.clear()
    menu_principal(page,name)
    Herramienta_Cliente(page)
    page.update()
    
def proveedor(e, page: ft.Page,name):
    page.controls.clear()
    menu_principal(page,name)
    Herramienta_Provedor(page)
    page.update()

def empleado(e, page: ft.Page,name):
    page.controls.clear()
    menu_principal(page,name)
    Herramienta_Empleado(page)
    page.update()

def usuario(e, page: ft.Page,name):
    page.controls.clear()
    menu_principal(page,name)
    Herramienta_Usuario(page)
    page.update()

def Repuesto(e, page: ft.Page,name):
    page.controls.clear()
    menu_principal(page,name)
    Herramienta_Repuesto(page)
    page.update()

def log(page: ft.Page):
    page.title = "Login"

    Email = ft.TextField(label="Email")
    Password = ft.TextField(label="Contraseña", password=True, can_reveal_password=True)

    def login(e):
        conn = connect_to_db()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT nombre
                FROM Usuarios
                WHERE email=%s AND contraseña=%s
            """, (Email.value, Password.value))
            resultado = cursor.fetchone()
        except Exception as ex:
            print("Error: ", ex)
            resultado = None
        finally:
            cursor.close()
            conn.close()

        if resultado:
            page.session.set("usuario", resultado[0])
            page.controls.clear()
            menu_principal(page,resultado[0])
            
        else:
            print("Email o contraseña incorrectos")
        page.update()

    page.add(
        ft.Text("Login", size=24, weight="bold"),
        Email,
        Password,
        ft.ElevatedButton("Aceptar", on_click=login)
    )


ft.app(target=log)
#ft.app(main, view=ft.AppView.WEB_BROWSER)