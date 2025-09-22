import flet as ft
import mysql.connector

def conectar_bd():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="TallerMecanico"
    )

class Persona:
    def insertar_Personas(dni, nombre, apellido, tel, dir_):
        conn = conectar_bd()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Persona (dni, nombre, apellido, tel, dir) VALUES (%s, %s, %s, %s, %s)",
                       (dni, nombre, apellido, tel, dir_))
            conn.commit()
        except Exception as e:
            print("Error al insertar Persona:", e)

    def eliminar_Personas(c):
    
        conn = conectar_bd()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Persona WHERE dni = %s", (c,))
            conn.commit()
        except Exception as e:
            print("Error al eliminar Persona:", e)

    def actualizar_Personas(dni, nombre, apellido, tel, dir_):
        conn = conectar_bd()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE Persona SET nombre=%s, apellido=%s, tel=%s, dir=%s WHERE dni=%s
            """, (nombre, apellido, tel, dir_, dni))
            conn.commit()
        except Exception as e:
            print("Error al actualizar Cliente:", e)

class cliente(Persona):
    def get_options():
        with conectar_bd() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT cod_Cliente FROM Cliente ORDER BY cod_Cliente")
                resultados = cursor.fetchall()
                return [ft.dropdown.Option(nombre[0]) for nombre in resultados]

    def obtener_Cliente_filtrada(nombre):
        with conectar_bd() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                SELECT c.cod_Cliente, p.dni, p.nombre, p.apellido, p.tel, p.dir
                FROM Cliente c
                JOIN Persona p ON c.dni_Cliente = p.dni
                WHERE c.cod_Cliente LIKE %s
                """, (nombre,))
                return cursor.fetchall()

    def obtener_Cliente():
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute("""
        SELECT c.cod_Cliente, p.dni, p.nombre, p.apellido, p.tel, p.dir
        FROM Cliente c
        JOIN Persona p ON c.dni_Cliente = p.dni
        """)
        resultados = cursor.fetchall()
        cursor.close()
        conn.close()
        return resultados

    def insertar_Cliente(dni, nombre, apellido, tel, dir_):
        conn = conectar_bd()
        cursor = conn.cursor()
        try:
            Persona.insertar_Personas(dni, nombre, apellido, tel, dir_)
            cursor.execute("INSERT INTO Cliente (dni_Cliente) VALUES (%s)",
                       (dni,))
            conn.commit()
        except Exception as e:
            print("Error al insertar Cliente:", e)
        finally:
            cursor.close()
            conn.close()

    def eliminar_Cliente(c):
    
        conn = conectar_bd()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Vehiculo WHERE dni_cliente = %s", (c[1],))
            cursor.execute("DELETE FROM Cliente WHERE dni_Cliente = %s", (c[1],))
            Persona.eliminar_Personas(c[1])
            conn.commit()
        except Exception as e:
            print("Error al eliminar Cliente:", e)
        finally:
            cursor.close()
            conn.close()

    def actualizar_Cliente(dni, nombre, apellido, tel, dir_):
        Persona.actualizar_Personas(nombre, apellido, tel, dir_, dni)

class Empleados(Persona):

    def get_options():
        with conectar_bd() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT legajo FROM Empleado ORDER BY legajo")
                resultados = cursor.fetchall()
                return [ft.dropdown.Option(nombre[0]) for nombre in resultados]

    def obtener_Empleado_filtrada(nombre):
        with conectar_bd() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                SELECT c.legajo, p.dni, p.nombre, p.apellido, p.tel, p.dir
                FROM Empleado c
                JOIN Persona p ON c.dni_Empleado = p.dni
                WHERE c.legajo LIKE %s
                """, (nombre,))
            return cursor.fetchall()

    def obtener_Empleado():
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute("""
        SELECT c.legajo, p.dni, p.nombre, p.apellido, p.tel, p.dir
        FROM Empleado c
        JOIN Persona p ON c.dni_Empleado = p.dni
        """)
        resultados = cursor.fetchall()
        cursor.close()
        conn.close()
        return resultados

    def insertar_Empleado(dni, nombre, apellido, tel, dir_):
        conn = conectar_bd()
        cursor = conn.cursor()
        try:
            Persona.insertar_Personas(dni, nombre, apellido, tel, dir_)
            cursor.execute("INSERT INTO Empleado (dni_Empleado) VALUES (%s)",
                       (dni,))
            conn.commit()
        except Exception as e:
            print("Error al insertar Empleado:", e)
        finally:
            cursor.close()
            conn.close()

    def eliminar_Empleado(c):
        
        conn = conectar_bd()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Usuarios WHERE legajo = %s", (c[0],))
            cursor.execute("DELETE FROM Empleado WHERE dni_Empleado = %s", (c[1],))
            Persona.eliminar_Personas(c[1])
            conn.commit()
        except Exception as e:
            print("Error al eliminar Empleado:", e)
        finally:
            cursor.close()
            conn.close()

    def actualizar_Empleado(legajo, dni, nombre, apellido, tel, dir_):
        conn = conectar_bd()
        cursor = conn.cursor()
        try:
            Persona.actualizar_Personas(nombre, apellido, tel, dir_, dni)
            cursor.execute("""
                UPDATE Usuarios SET nombre=%s WHERE legajo=%s
            """, (nombre,legajo ))
            conn.commit()

        except Exception as e:
            print("Error al actualizar Empleado:", e)
        finally:
            cursor.close()
            conn.close()

class Provedores(Persona):
    def get_options():
        with conectar_bd() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT cod_Provedor FROM Provedor ORDER BY cod_Provedor")
                resultados = cursor.fetchall()
                return [ft.dropdown.Option(nombre[0]) for nombre in resultados]

    def obtener_Provedor_filtrada(nombre):
        with conectar_bd() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT c.cod_Provedor, p.dni, p.nombre, p.apellido, p.tel, p.dir
                    FROM Provedor c
                    JOIN Persona p ON c.dni_Provedor = p.dni
                    WHERE c.cod_Provedor LIKE %s
                """, (nombre,))
                return cursor.fetchall()

    def obtener_Provedor():
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.cod_Provedor, p.dni, p.nombre, p.apellido, p.tel, p.dir
            FROM Provedor c
            JOIN Persona p ON c.dni_Provedor = p.dni
        """)
        resultados = cursor.fetchall()
        cursor.close()
        conn.close()
        return resultados

    def insertar_Provedor(dni, nombre, apellido, tel, dir_):
        conn = conectar_bd()
        cursor = conn.cursor()
        try:
            Persona.insertar_Personas(dni, nombre, apellido, tel, dir_)
            cursor.execute("INSERT INTO Provedor (dni_Provedor) VALUES (%s)",
                        (dni,))
            conn.commit()
        except Exception as e:
            print("Error al insertar Provedor:", e)
        finally:
            cursor.close()
            conn.close()

    def eliminar_Provedor(c):
        
        conn = conectar_bd()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Provedor WHERE dni_Provedor = %s", (c[1],))
            Persona.eliminar_Personas(c[1])
            conn.commit()
        except Exception as e:
            print("Error al eliminar Provedor:", e)
        finally:
            cursor.close()
            conn.close()

    def actualizar_Provedor(cod_Provedor, dni, nombre, apellido, tel, dir_):
        Persona.actualizar_Personas(nombre, apellido, tel, dir_, dni)

class Repuestos:
    def get_options():
        with conectar_bd() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT nombre FROM Repuesto ORDER BY nombre")
                resultados = cursor.fetchall()
                return [ft.dropdown.Option(nombre[0]) for nombre in resultados]

    def obtener_Repuesto_filtrada(nombre):
        with conectar_bd() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT nombre, precio_x_unidad, cantidad
                    FROM Repuesto
                    WHERE nombre LIKE %s
                """, (f"%{nombre}%",))
                return cursor.fetchall()

    def obtener_Repuesto():
        with conectar_bd() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT nombre, precio_x_unidad, cantidad FROM Repuesto")
                return cursor.fetchall()

    def insertar_repuesto(nombre, precio_x_unidad, cantidad):
        with conectar_bd() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO Repuesto (nombre, precio_x_unidad, cantidad)
                    VALUES (%s, %s, %s)
                """, (nombre, precio_x_unidad, cantidad))
                conn.commit()

    def eliminar_repuesto(nombre):
        with conectar_bd() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM Repuesto WHERE nombre = %s", (nombre,))
                conn.commit()

    def actualizar_repuesto(nombre, precio_x_unidad, cantidad):
        with conectar_bd() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE Repuesto
                    SET precio_x_unidad=%s, cantidad=%s
                    WHERE nombre=%s
                """, (precio_x_unidad, cantidad, nombre))
                conn.commit()

class Usuarios:
    def get_options_legajos():
        with conectar_bd() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT legajo FROM Empleado ORDER BY legajo")
                resultados = cursor.fetchall()
                return [ft.dropdown.Option(nombre[0]) for nombre in resultados]

    def get_options():
        with conectar_bd() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT email FROM Usuarios ORDER BY email")
                resultados = cursor.fetchall()
                return [ft.dropdown.Option(email[0]) for email in resultados]

    def obtener_Usuario_filtrada(email):
        with conectar_bd() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT * FROM Usuarios
                    WHERE email LIKE %s
                """, (f"%{email}%",))
                return cursor.fetchall()

    def obtener_Usuario():
        with conectar_bd() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM Usuarios")
                return cursor.fetchall()

    def insertar_Usuario(email, contraseña,legajo):

        with conectar_bd() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT dni_empleado 
                    FROM Empleado
                    WHERE legajo=%s
                """, (legajo,))
                dni=cursor.fetchone()
                print("\nsadsadsaasdasd")
                cursor.execute("""
                    SELECT nombre 
                    FROM Persona
                    WHERE dni=%s
                """, (dni[0],))
                
                nombre=cursor.fetchone()
                cursor.execute("""
                    INSERT INTO Usuarios 
                    VALUES (%s, %s, %s,%s)
                """, (email, nombre[0], contraseña,legajo))
                conn.commit()

    def eliminar_Usuario(email):
        with conectar_bd() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM Usuarios WHERE email = %s", (email,))
                conn.commit()

    def actualizar_Usuario(email, contraseña,legajo):
        with conectar_bd() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE Usuarios
                    SET contraseña=%s, legajo=%s
                    WHERE email=%s
                """, (contraseña,legajo, email))
                conn.commit()

    def Login(Email,Password):
        with conectar_bd() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT nombre
                    FROM Usuarios
                    WHERE email=%s AND contraseña=%s
                """, (Email, Password))
                resultado = cursor.fetchone()
                cursor.close()
                conn.close()
                return resultado

class Vehiculos:
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

class Presupuestos:
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

