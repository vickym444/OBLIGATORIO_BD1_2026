from database.connection import get_connection


class UsuarioRepository:
    def get_all_usuarios(self):
        connection = get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT id_usuario, username, rol, id_estudiante, activo
                FROM usuario
                WHERE activo = 1
                ORDER BY id_usuario
                """
            )
            return cursor.fetchall()
        finally:
            connection.close()

    def get_usuario_by_id(self, id_usuario):
        connection = get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT id_usuario, username, rol, id_estudiante, activo
                FROM usuario
                WHERE id_usuario = %s
                """,
                (id_usuario,)
            )
            return cursor.fetchone()
        finally:
            connection.close()

    def get_usuario_by_username(self, username):
        connection = get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT id_usuario, username, rol, id_estudiante, activo
                FROM usuario
                WHERE username = %s
                """,
                (username,)
            )
            return cursor.fetchone()
        finally:
            connection.close()

    def create_usuario(self, username, password_hash, rol, id_estudiante, activo=1):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                INSERT INTO usuario (username, password_hash, rol, id_estudiante, activo)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (username, password_hash, rol, id_estudiante, activo)
            )
            connection.commit()
            return cursor.lastrowid
        finally:
            connection.close()

    def update_usuario(self, id_usuario, username, password_hash, rol, id_estudiante, activo):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                UPDATE usuario
                SET username = %s,
                    password_hash = %s,
                    rol = %s,
                    id_estudiante = %s,
                    activo = %s
                WHERE id_usuario = %s
                """,
                (username, password_hash, rol, id_estudiante, activo, id_usuario)
            )
            connection.commit()
            return cursor.rowcount
        finally:
            connection.close()

    def delete_usuario(self, id_usuario):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                UPDATE usuario
                SET activo = 0
                WHERE id_usuario = %s
                """,
                (id_usuario,)
            )
            connection.commit()
            return cursor.rowcount
        finally:
            connection.close()