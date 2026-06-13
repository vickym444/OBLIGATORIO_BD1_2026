from database.connection import get_connection


class FacultadRepository:
    def get_all_facultades(self):
        connection = get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT id_facultad, nombre
                FROM facultad
                ORDER BY id_facultad
                """
            )
            return cursor.fetchall()
        finally:
            connection.close()

    def get_facultad_by_id(self, id_facultad):
        connection = get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT id_facultad, nombre
                FROM facultad
                WHERE id_facultad = %s
                """,
                (id_facultad,)
            )
            return cursor.fetchone()
        finally:
            connection.close()

    def create_facultad(self, nombre):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                INSERT INTO facultad (nombre)
                VALUES (%s)
                """,
                (nombre,)
            )
            connection.commit()
            return cursor.lastrowid
        finally:
            connection.close()

    def update_facultad(self, id_facultad, nombre):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                UPDATE facultad
                SET nombre = %s
                WHERE id_facultad = %s
                """,
                (nombre, id_facultad)
            )
            connection.commit()
            return cursor.rowcount
        finally:
            connection.close()

    def delete_facultad(self, id_facultad):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                UPDATE facultad
                SET activo = 0
                WHERE id_facultad = %s
                """,
                (id_facultad,)
            )
            connection.commit()
            return cursor.rowcount
        finally:
            connection.close()