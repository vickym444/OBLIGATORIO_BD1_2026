from database.connection import get_connection


class EstudianteRepository:
    def get_all_estudiantes(self):
        connection = get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT id_estudiante, documento, nombre, apellido, email, activo, id_carrera
                FROM estudiante
                ORDER BY id_estudiante
                """
            )
            return cursor.fetchall()
        finally:
            connection.close()

    def get_estudiante_by_id(self, id_estudiante):
        connection = get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT id_estudiante, documento, nombre, apellido, email, activo, id_carrera
                FROM estudiante
                WHERE id_estudiante = %s
                """,
                (id_estudiante,)
            )
            return cursor.fetchone()
        finally:
            connection.close()

    def create_estudiante(self, documento, nombre, apellido, email, id_carrera, activo=1):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                INSERT INTO estudiante (documento, nombre, apellido, email, activo, id_carrera)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (documento, nombre, apellido, email, activo, id_carrera)
            )
            connection.commit()
            return cursor.lastrowid
        finally:
            connection.close()

    def update_estudiante(self, id_estudiante, documento, nombre, apellido, email, activo, id_carrera):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                UPDATE estudiante
                SET documento = %s,
                    nombre = %s,
                    apellido = %s,
                    email = %s,
                    activo = %s,
                    id_carrera = %s
                WHERE id_estudiante = %s
                """,
                (documento, nombre, apellido, email, activo, id_carrera, id_estudiante)
            )
            connection.commit()
            return cursor.rowcount
        finally:
            connection.close()

    def delete_estudiante(self, id_estudiante):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                UPDATE estudiante
                SET activo = 0
                WHERE id_estudiante = %s
                """,
                (id_estudiante,)
            )
            connection.commit()
            return cursor.rowcount
        finally:
            connection.close()