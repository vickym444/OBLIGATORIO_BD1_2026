from database.connection import get_connection


class DisciplinaRepository:
    def get_all_disciplinas(self):
        connection = get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT id_disciplina, nombre, descripcion, activo
                FROM disciplina
                WHERE activo = 1
                ORDER BY id_disciplina
                """
            )
            return cursor.fetchall()
        finally:
            connection.close()

    def get_disciplina_by_id(self, id_disciplina):
        connection = get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT id_disciplina, nombre, descripcion, activo
                FROM disciplina
                WHERE id_disciplina = %s
                """,
                (id_disciplina,)
            )
            return cursor.fetchone()
        finally:
            connection.close()

    def get_disciplina_by_nombre(self, nombre):
        connection = get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT id_disciplina, nombre, descripcion, activo
                FROM disciplina
                WHERE nombre = %s
                """,
                (nombre,)
            )
            return cursor.fetchone()
        finally:
            connection.close()

    def create_disciplina(self, nombre, descripcion):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                INSERT INTO disciplina (nombre, descripcion, activo)
                VALUES (%s, %s, 1)
                """,
                (nombre, descripcion)
            )
            connection.commit()
            return cursor.lastrowid
        finally:
            connection.close()

    def reactivate_disciplina(self, id_disciplina):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                UPDATE disciplina
                SET activo = 1
                WHERE id_disciplina = %s
                """,
                (id_disciplina,)
            )
            connection.commit()
            return cursor.rowcount
        finally:
            connection.close()

    def update_disciplina(self, id_disciplina, nombre, descripcion, activo):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                UPDATE disciplina
                SET nombre = %s,
                    descripcion = %s,
                    activo = %s
                WHERE id_disciplina = %s
                """,
                (nombre, descripcion, activo, id_disciplina)
            )
            connection.commit()
            return cursor.rowcount
        finally:
            connection.close()

    def delete_disciplina(self, id_disciplina):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                UPDATE disciplina
                SET activo = 0
                WHERE id_disciplina = %s
                """,
                (id_disciplina,)
            )
            connection.commit()
            return cursor.rowcount
        finally:
            connection.close()