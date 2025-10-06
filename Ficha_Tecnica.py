import flet as ft
import mysql.connector
from classes import FichaTecnica

def conectar_bd():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="TallerMecanico"
    )



def Herramienta_Ficha_Tecnica(page: ft.Page):
    page.title = "Gestion de Ficha_Tecnica"
    page.scroll = ft.ScrollMode.AUTO

    tabla = ft.Column()


    def cargar_tabla():
        datos = FichaTecnica.obtener_FichaTecnica()
        tabla.controls.clear()
        tabla.controls.append(ft.Row([
                        ft.Text("id"),
                        ft.Text("Matricula"),
                        ft.Text("nroEmpleados"),
                        ft.Text("subtotal"),
                        ft.Text("mano_de_obra"),
                        ft.Text("total"),       
                ])
            )
        print(datos)
        for c in datos:
                tabla.controls.append(ft.Row([
                        ft.Text(str(c[0])),
                        ft.Text(str(c[1])),
                        ft.Text(str(c[2])),
                        ft.Text(str(c[3])),
                        ft.Text(str(c[4])),
                        ft.Text(str(c[5])),                
                ])
            )
        page.update()

    Row=ft.Row([tabla])
    
    page.add(
        ft.Text("Ficha_Tecnica", size=24, weight="bold"),
        ft.Divider(),
        Row)

    cargar_tabla()

if __name__ == "__Herramienta_Ficha_Tecnica__":
    ft.app(target=Herramienta_Ficha_Tecnica)
