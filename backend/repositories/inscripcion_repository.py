from database.connection import get_connection


class InscripcionRepository:
    def get_all_inscripciones(self):
        connection = get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT i.id_inscripcion, i.fecha_inscripcion, i.fecha_baja,
                       i.estado, i.id_estudiante, i.id_practica
                FROM inscripcion i
                WHERE i.fecha_baja IS NULL
                ORDER BY i.id_inscripcion
                """
            )
            return cursor.fetchall()
        finally:
            connection.close()

    def get_inscripcion_by_id(self, id_inscripcion):
        connection = get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT id_inscripcion, fecha_inscripcion, fecha_baja,
                       estado, id_estudiante, id_practica
                FROM inscripcion
                WHERE id_inscripcion = %s
                """,
                (id_inscripcion,)
            )
            return cursor.fetchone()
        finally:
            connection.close()

    def get_inscripciones_by_estudiante(self, id_estudiante):
        connection = get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT id_inscripcion, fecha_inscripcion, fecha_baja,
                       estado, id_estudiante, id_practica
                FROM inscripcion
                WHERE id_estudiante = %s AND fecha_baja IS NULL
                ORDER BY fecha_inscripcion
                """,
                (id_estudiante,)
            )
            return cursor.fetchall()
        finally:
            connection.close()

    def get_inscripciones_by_practica(self, id_practica):
        connection = get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT id_inscripcion, fecha_inscripcion, fecha_baja,
                       estado, id_estudiante, id_practica
                FROM inscripcion
                WHERE id_practica = %s AND fecha_baja IS NULL
                ORDER BY fecha_inscripcion
                """,
                (id_practica,)
            )
            return cursor.fetchall()
        finally:
            connection.close()

    def get_inscripcion_activa(self, id_estudiante, id_practica):
        connection = get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT id_inscripcion
                FROM inscripcion
                WHERE id_estudiante = %s
                  AND id_practica = %s
                  AND fecha_baja IS NULL
                """,
                (id_estudiante, id_practica)
            )
            return cursor.fetchone()
        finally:
            connection.close()

    def count_inscripciones_activas(self, id_practica):
        connection = get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT COUNT(*) as total
                FROM inscripcion
                WHERE id_practica = %s AND fecha_baja IS NULL
                """,
                (id_practica,)
            )
            return cursor.fetchone()["total"]
        finally:
            connection.close()

    def create_inscripcion(self, fecha_inscripcion, estado, id_estudiante, id_practica):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                INSERT INTO inscripcion (fecha_inscripcion, fecha_baja, estado, id_estudiante, id_practica)
                VALUES (%s, NULL, %s, %s, %s)
                """,
                (fecha_inscripcion, estado, id_estudiante, id_practica)
            )
            connection.commit()
            return cursor.lastrowid
        finally:
            connection.close()

    def update_estado(self, id_inscripcion, estado):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                UPDATE inscripcion
                SET estado = %s
                WHERE id_inscripcion = %s
                """,
                (estado, id_inscripcion)
            )
            connection.commit()
            return cursor.rowcount
        finally:
            connection.close()

    def dar_baja(self, id_inscripcion, fecha_baja):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                UPDATE inscripcion
                SET fecha_baja = %s,
                    estado = 'cancelada'
                WHERE id_inscripcion = %s
                """,
                (fecha_baja, id_inscripcion)
            )
            connection.commit()
            return cursor.rowcount
        finally:
            connection.close()