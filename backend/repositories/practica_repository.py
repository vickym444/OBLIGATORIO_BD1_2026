from database.connection import get_connection


class PracticaRepository:
    def get_all_practicas(self):
        connection = get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT id_practica, id_actividad, fecha, activo
                FROM practica
                WHERE activo = 1
                ORDER BY id_practica
                """
            )
            return cursor.fetchall()
        finally:
            connection.close()

    def get_practicas_by_actividad(self, id_actividad):
        connection = get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT id_practica, id_actividad, fecha, activo
                FROM practica
                WHERE id_actividad = %s AND activo = 1
                ORDER BY fecha
                """,
                (id_actividad,)
            )
            return cursor.fetchall()
        finally:
            connection.close()

    def get_practica_by_id(self, id_practica):
        connection = get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT id_practica, id_actividad, fecha, activo
                FROM practica
                WHERE id_practica = %s
                """,
                (id_practica,)
            )
            return cursor.fetchone()
        finally:
            connection.close()

    def create_practica(self, id_actividad, fecha):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                INSERT INTO practica (id_actividad, fecha, activo)
                VALUES (%s, %s, 1)
                """,
                (id_actividad, fecha)
            )
            connection.commit()
            return cursor.lastrowid
        finally:
            connection.close()

    def update_practica(self, id_practica, id_actividad, fecha, activo):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                UPDATE practica
                SET id_actividad = %s,
                    fecha = %s,
                    activo = %s
                WHERE id_practica = %s
                """,
                (id_actividad, fecha, activo, id_practica)
            )
            connection.commit()
            return cursor.rowcount
        finally:
            connection.close()

    def delete_practica(self, id_practica):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                UPDATE practica
                SET activo = 0
                WHERE id_practica = %s
                """,
                (id_practica,)
            )
            connection.commit()
            return cursor.rowcount
        finally:
            connection.close()