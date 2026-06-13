from database.connection import get_connection


class AsistenciaRepository:
    def get_all_asistencias(self):
        connection = get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT id_asistencia, presente, id_inscripcion
                FROM asistencia
                ORDER BY id_asistencia
                """
            )
            return cursor.fetchall()
        finally:
            connection.close()

    def get_asistencia_by_id(self, id_asistencia):
        connection = get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT id_asistencia, presente, id_inscripcion
                FROM asistencia
                WHERE id_asistencia = %s
                """,
                (id_asistencia,)
            )
            return cursor.fetchone()
        finally:
            connection.close()

    def get_asistencia_by_inscripcion(self, id_inscripcion):
        connection = get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT id_asistencia, presente, id_inscripcion
                FROM asistencia
                WHERE id_inscripcion = %s
                """,
                (id_inscripcion,)
            )
            return cursor.fetchone()
        finally:
            connection.close()

    def create_asistencia(self, presente, id_inscripcion):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                INSERT INTO asistencia (presente, id_inscripcion)
                VALUES (%s, %s)
                """,
                (presente, id_inscripcion)
            )
            connection.commit()
            return cursor.lastrowid
        finally:
            connection.close()

    def update_asistencia(self, id_asistencia, presente):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                UPDATE asistencia
                SET presente = %s
                WHERE id_asistencia = %s
                """,
                (presente, id_asistencia)
            )
            connection.commit()
            return cursor.rowcount
        finally:
            connection.close()