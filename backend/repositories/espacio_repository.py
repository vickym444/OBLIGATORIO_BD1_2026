from database.connection import get_connection


class EspacioRepository:
    def get_all_espacios(self):
        connection = get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT id_espacio, nombre, descripcion, activo
                FROM espacio
                WHERE activo = 1
                ORDER BY id_espacio
                """
            )
            return cursor.fetchall()
        finally:
            connection.close()

    def get_espacio_by_id(self, id_espacio):
        connection = get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT id_espacio, nombre, descripcion, activo
                FROM espacio
                WHERE id_espacio = %s
                """,
                (id_espacio,)
            )
            return cursor.fetchone()
        finally:
            connection.close()

    def create_espacio(self, nombre, descripcion):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                INSERT INTO espacio (nombre, descripcion, activo)
                VALUES (%s, %s, 1)
                """,
                (nombre, descripcion)
            )
            connection.commit()
            return cursor.lastrowid
        finally:
            connection.close()

    def update_espacio(self, id_espacio, nombre, descripcion, activo):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                UPDATE espacio
                SET nombre = %s,
                    descripcion = %s,
                    activo = %s
                WHERE id_espacio = %s
                """,
                (nombre, descripcion, activo, id_espacio)
            )
            connection.commit()
            return cursor.rowcount
        finally:
            connection.close()

    def delete_espacio(self, id_espacio):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                UPDATE espacio
                SET activo = 0
                WHERE id_espacio = %s
                """,
                (id_espacio,)
            )
            connection.commit()
            return cursor.rowcount
        finally:
            connection.close()