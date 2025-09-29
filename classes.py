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
    def __init__(self, dni, nombre, apellido, tel, dir_):
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido
        self.tel = tel
        self.dir_ = dir_

    def insertar(self):
        conn = conectar_bd()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO Persona (dni, nombre, apellido, tel, dir) VALUES (%s, %s, %s, %s, %s)",
                (self.dni, self.nombre, self.apellido, self.tel, self.dir_)
            )
            conn.commit()
        except Exception as e:
            print("Error al insertar Persona:", e)
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def eliminar_Personas(dni):
        conn = conectar_bd()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Persona WHERE dni = %s", (dni,))
            conn.commit()
        except Exception as e:
            print("Error al eliminar Persona:", e)
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def actualizar_Personas(dni, nombre, apellido, tel, dir_):
        conn = conectar_bd()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE Persona 
                SET nombre=%s, apellido=%s, tel=%s, dir=%s 
                WHERE dni=%s
            """, (nombre, apellido, tel, dir_, dni))
            conn.commit()
        except Exception as e:
            print("Error al actualizar Persona:", e)
        finally:
            cursor.close()
            conn.close()

class cliente(Persona):   
    def __init__(self, dni, nombre, apellido, tel, dir_):
        super().__init__(dni, nombre, apellido, tel, dir_)
        self.insertar()

    def insertar(self):
        super().insertar()
        conn = conectar_bd()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Cliente (dni_Cliente) VALUES (%s)", (self.dni,))
            conn.commit()
        except Exception as e:
            print("Error al insertar Cliente:", e)
        finally:
            cursor.close()
            conn.close()
                             
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

class Empleados(Persona):
    def __init__(self, dni, nombre, apellido, tel, dir_):
        super().__init__(dni, nombre, apellido, tel, dir_)
        self.insertar()

    def insertar(self):
        super().insertar()
        conn = conectar_bd()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Empleado (dni_Empleado) VALUES (%s)", (self.dni,))
            conn.commit()
        except Exception as e:
            print("Error al insertar Cliente:", e)
        finally:
            cursor.close()
            conn.close()
        
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

class Provedores(Persona):
    def __init__(self, dni, nombre, apellido, tel, dir_):
        super().__init__(dni, nombre, apellido, tel, dir_)
        self.insertar()

    def insertar(self):
        super().insertar()
        conn = conectar_bd()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Provedor (dni_Provedor) VALUES (%s)", (self.dni,))
            conn.commit()
        except Exception as e:
            print("Error al insertar Cliente:", e)
        finally:
            cursor.close()
            conn.close()


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

    def insertar_Presupuestos(matricula, repuesto, cantidad, legajo, precio, id=None):
        conn = conectar_bd()
        cursor = conn.cursor()
        try:
            if id is None:
                cursor.execute(
                    "INSERT INTO Reparaciones (matricula_vehiculo) VALUES (%s)",
                    (matricula,)
                )
                cursor.execute("SELECT MAX(id) FROM Reparaciones")
                id = cursor.fetchone()[0]

            cursor.execute(
                """INSERT INTO detalle_Reparacion
                (reparacion_id, legajo, repuesto, cantidad, precio)
                VALUES (%s, %s, %s, %s, %s)""",
                (id, legajo, repuesto, cantidad, precio)
            )

            conn.commit()
        except Exception as e:
            print("Error al insertar Presupuesto:", e)
        finally:
            cursor.close()
            conn.close()
        return id

    def obtener_Presupuesto(id):
        resultado = []
        with conectar_bd() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM Reparaciones WHERE id=%s", (id,))
                resultado.append(cursor.fetchone())

                cursor.execute("SELECT * FROM detalle_Reparacion WHERE reparacion_id=%s", (id,))
                resultado.append(cursor.fetchall())
        return resultado

    def eliminar_Presupuesto(id):
        with conectar_bd() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM detalle_Reparacion WHERE reparacion_id=%s", (id,))
                conn.commit()
                
    def eliminar_Todo_Presupuesto(id):
        with conectar_bd() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM Reparaciones WHERE id=%s", (id,))
                conn.commit()

    def actualizar_Presupuesto(repuesto, cantidad, legajo, precio, id):
        with conectar_bd() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE detalle_Reparacion
                    SET repuesto=%s, cantidad=%s legajo=%s precio=%s
                    WHERE id=%s
                """, (repuesto, cantidad, legajo, precio,id))
                conn.commit()