from database.connection import get_connection


class CarreraRepository:
    def get_all_carreras(self):
        connection = get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT id_carrera, nombre, id_facultad, activo
                FROM carrera
                WHERE activo = 1
                ORDER BY id_carrera
                """
            )
            return cursor.fetchall()
        finally:
            connection.close()

    def get_carrera_by_id(self, id_carrera):
        connection = get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT id_carrera, nombre, id_facultad, activo
                FROM carrera
                WHERE id_carrera = %s
                """,
                (id_carrera,)
            )
            return cursor.fetchone()
        finally:
            connection.close()

    def get_carrera_by_nombre_inactiva(self, nombre):
        connection = get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT id_carrera, nombre, id_facultad, activo
                FROM carrera
                WHERE nombre = %s AND activo = 0
                """,
                (nombre,)
            )
            return cursor.fetchone()
        finally:
            connection.close()

    def reactivate_carrera(self, id_carrera):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                UPDATE carrera
                SET activo = 1
                WHERE id_carrera = %s
                """,
                (id_carrera,)
            )
            connection.commit()
            return cursor.rowcount
        finally:
            connection.close()
            
    def create_carrera(self, nombre, id_facultad, activo=1):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                INSERT INTO carrera (nombre, id_facultad, activo)
                VALUES (%s, %s, %s)
                """,
                (nombre, id_facultad, activo)
            )
            connection.commit()
            return cursor.lastrowid
        finally:
            connection.close()

    def update_carrera(self, id_carrera, nombre, id_facultad, activo):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                UPDATE carrera
                SET nombre = %s,
                    id_facultad = %s,
                    activo = %s
                WHERE id_carrera = %s
                """,
                (nombre, id_facultad, activo, id_carrera)
            )
            connection.commit()
            return cursor.rowcount
        finally:
            connection.close()

    def delete_carrera(self, id_carrera):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                UPDATE carrera
                SET activo = 0
                WHERE id_carrera = %s
                """,
                (id_carrera,)
            )
            connection.commit()
            return cursor.rowcount
        finally:
            connection.close()