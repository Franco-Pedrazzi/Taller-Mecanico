import flet as ft
import mysql.connector

#--Importar los archivos correspondiente al sistema con las clases

from cliente import Herramienta_Cliente
from Empleado import Herramienta_empleado
from Provedor import Herramienta_Provedor
from Repuesto import Herramienta_Repuesto
from usuario import Herramienta_Usuario
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
            print('Conexión exitosa')
            return connection
    except Exception as ex:
        print('Conexión errónea')
        print(ex)
        return None

connection = connect_to_db()




def menu_principal(page: ft.Page):
    page.window.maximized=True
    page.title = "Administración de Taller Mecánico"

    cliente_icono = ft.Image(src="/home/usuario/Desktop/FP/programacion/Flet/Taller-Mecanico/iconos/usuario.png", width=28, height=28)
    cliente_item = ft.Row(
        controls=[
            cliente_icono,
            ft.Text("Cliente"),
        ],
        alignment=ft.MainAxisAlignment.START,
        spacing=8
    )
    
    proveedor_icono = ft.Image(src="/home/usuario/Desktop/FP/programacion/Flet/Taller-Mecanico/iconos/proveedor.png", width=28, height=28)
    proveedor_item = ft.Row(
        controls=[
            proveedor_icono,
            ft.Text("Proveedor"),
        ],
        alignment=ft.MainAxisAlignment.START,
        spacing=8
    )
    
    repuesto_icono = ft.Image(src="/home/usuario/Desktop/FP/programacion/Flet/Taller-Mecanico/iconos/caja-de-cambios.png", width=28, height=28)  
    repuesto_item = ft.Row(
        controls=[
            repuesto_icono,
            ft.Text("Repuesto"),
        ],
        alignment=ft.MainAxisAlignment.START,
        spacing=8
    )
    
    empleado_icono = ft.Image(src="/home/usuario/Desktop/FP/programacion/Flet/Taller-Mecanico/iconos/empleado.png", width=28, height=28)  
    empleado_item = ft.Row(
        controls=[
            empleado_icono,
            ft.Text("Empleado"),
        ],
        alignment=ft.MainAxisAlignment.START,
        spacing=8
    ) 
    
    usuario_icono = ft.Image(src="/home/usuario/Desktop/FP/programacion/Flet/Taller-Mecanico/iconos/usuarios.png", width=28, height=28)  
    usuario_item = ft.Row(
        controls=[
            usuario_icono,
            ft.Text("Usuario"),
        ],
        alignment=ft.MainAxisAlignment.START,
        spacing=8
    )
    
    ficha_tecnica_icono=ft.Image(src="/home/usuario/Desktop/FP/programacion/Flet/Taller-Mecanico/iconos/auto.png", width=28, height=28)
    ficha_tecnica_item=ft.Row(
        controls=[
            ficha_tecnica_icono,
            ft.Text("Ficha Técnica")
        ],
        alignment=ft.MainAxisAlignment.START,
        spacing=8
    )
    
    presupuesto_icono=ft.Image(src="/home/usuario/Desktop/FP/programacion/Flet/Taller-Mecanico/iconos/presupuesto.png", width=28, height=28)
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
            ft.PopupMenuItem(content=cliente_item, on_click=lambda e: cliente(e, page)),
            ft.PopupMenuItem(content=proveedor_item, on_click=lambda e:proveedor(e, page)),
            ft.PopupMenuItem(content=repuesto_item, on_click=lambda e: Repuesto(e, page)),
            ft.PopupMenuItem(content=empleado_item, on_click=lambda e: empleado(e, page)),
            ft.PopupMenuItem(content=usuario_item, on_click=lambda e: usuario(e, page)),
        ],
        content=ft.Text("Herramientas"), tooltip="Administrador de archivos maestros"
        
    )
    
    administracion = ft.PopupMenuButton(
        items=[
            ft.PopupMenuItem(content=ficha_tecnica_item),#, on_click=lambda e: cliente(e, page)),
            ft.PopupMenuItem(content=presupuesto_icono_item),#, on_click=lambda e:proveedor(e, page)),
        ],
        content=ft.Text("Administración"), tooltip="Administración de presupuesto y ficha técnica"
        
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
    boton_ficha_tecnica = ft.IconButton(content=boton_ficha_tecnica_item,tooltip="Ficha Técnica")

    boton_presupuesto_item=ft.Row(
        controls=[
            presupuesto_icono,
        ]
    )
    boton_presupuesto=ft.IconButton(content=boton_presupuesto_item,tooltip="Presupuesto")
    
    
    
    
    page.add(
        ft.Row(
            controls=[
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

def cliente(e, page: ft.Page):
    page.controls.clear()
    menu_principal(page)
    Herramienta_Cliente(page)
    page.update()
    
def proveedor(e, page: ft.Page):
    page.controls.clear()
    menu_principal(page)
    Herramienta_Provedor(page)
    page.update()

def empleado(e, page: ft.Page):
    page.controls.clear()
    menu_principal(page)
    Herramienta_empleado(page)
    page.update()

def usuario(e, page: ft.Page):
    page.controls.clear()
    menu_principal(page)
    Herramienta_Usuario(page)
    page.update()

def Repuesto(e, page: ft.Page):
    page.controls.clear()
    menu_principal(page)
    Herramienta_Repuesto(page)
    page.update()

def main(page: ft.Page):
    page.window.maximized = True
    menu_principal(page)

ft.app(target=main)
#ft.app(main, view=ft.AppView.WEB_BROWSER)