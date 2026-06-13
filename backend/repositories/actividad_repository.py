from database.connection import get_connection


class ActividadRepository:
    def get_all_actividades(self):
        connection = get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT id_actividad, nombre, cupo_maximo, cupo_minimo,
                       hora_inicio, hora_fin, dia, estado,
                       id_disciplina, id_espacio, activo
                FROM actividad
                WHERE activo = 1
                ORDER BY id_actividad
                """
            )
            return cursor.fetchall()
        finally:
            connection.close()

    def get_actividad_by_id(self, id_actividad):
        connection = get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT id_actividad, nombre, cupo_maximo, cupo_minimo,
                       hora_inicio, hora_fin, dia, estado,
                       id_disciplina, id_espacio, activo
                FROM actividad
                WHERE id_actividad = %s
                """,
                (id_actividad,)
            )
            return cursor.fetchone()
        finally:
            connection.close()

    def create_actividad(self, nombre, cupo_maximo, cupo_minimo, hora_inicio, hora_fin, dia, estado, id_disciplina, id_espacio):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                INSERT INTO actividad (nombre, cupo_maximo, cupo_minimo, hora_inicio, hora_fin, dia, estado, id_disciplina, id_espacio, activo)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 1)
                """,
                (nombre, cupo_maximo, cupo_minimo, hora_inicio, hora_fin, dia, estado, id_disciplina, id_espacio)
            )
            connection.commit()
            return cursor.lastrowid
        finally:
            connection.close()

    def update_actividad(self, id_actividad, nombre, cupo_maximo, cupo_minimo, hora_inicio, hora_fin, dia, estado, id_disciplina, id_espacio, activo):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                UPDATE actividad
                SET nombre = %s,
                    cupo_maximo = %s,
                    cupo_minimo = %s,
                    hora_inicio = %s,
                    hora_fin = %s,
                    dia = %s,
                    estado = %s,
                    id_disciplina = %s,
                    id_espacio = %s,
                    activo = %s
                WHERE id_actividad = %s
                """,
                (nombre, cupo_maximo, cupo_minimo, hora_inicio, hora_fin, dia, estado, id_disciplina, id_espacio, activo, id_actividad)
            )
            connection.commit()
            return cursor.rowcount
        finally:
            connection.close()

    def delete_actividad(self, id_actividad):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                UPDATE actividad
                SET activo = 0
                WHERE id_actividad = %s
                """,
                (id_actividad,)
            )
            connection.commit()
            return cursor.rowcount
        finally:
            connection.close()