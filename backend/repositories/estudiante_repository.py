from database.connection import get_connection


class EstudianteRepository:
    def get_all_estudiantes(self, solo_con_3_inasistencias=False):
        connection = get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            filtros = ["e.activo = 1"]
            if solo_con_3_inasistencias:
                filtros.append("COALESCE(ina.total_inasistencias, 0) >= 3")

            where_sql = "WHERE " + " AND ".join(filtros)
            order_sql = (
                "ORDER BY COALESCE(ina.total_inasistencias, 0) DESC, e.id_estudiante"
                if solo_con_3_inasistencias
                else "ORDER BY e.id_estudiante"
            )

            cursor.execute(
                f"""
                SELECT e.id_estudiante,
                       e.documento,
                       e.nombre,
                       e.apellido,
                       e.email,
                       e.activo,
                       e.id_carrera,
                       COALESCE(ina.total_inasistencias, 0) AS total_inasistencias
                FROM estudiante e
                LEFT JOIN (
                    SELECT i.id_estudiante,
                           COUNT(*) AS total_inasistencias
                    FROM inscripcion i
                    INNER JOIN practica p ON p.id_practica = i.id_practica
                    LEFT JOIN asistencia a ON a.id_inscripcion = i.id_inscripcion
                    WHERE i.fecha_baja IS NULL
                      AND i.estado = 'confirmada'
                      AND p.fecha < CURDATE()
                      AND (a.id_asistencia IS NULL OR a.presente = 0)
                    GROUP BY i.id_estudiante
                ) ina ON ina.id_estudiante = e.id_estudiante
                {where_sql}
                {order_sql}
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

    def get_estudiante_by_documento(self, documento):
        connection = get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT id_estudiante, documento, nombre, apellido, email, activo, id_carrera
                FROM estudiante
                WHERE documento = %s
                """,
                (documento,)
            )
            return cursor.fetchone()
        finally:
            connection.close()

    def get_estudiante_by_email(self, email):
        connection = get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT id_estudiante, documento, nombre, apellido, email, activo, id_carrera
                FROM estudiante
                WHERE email = %s
                """,
                (email,)
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