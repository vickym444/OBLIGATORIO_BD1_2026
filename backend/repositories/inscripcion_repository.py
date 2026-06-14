from database.connection import get_connection


class InscripcionRepository:
    def get_all_inscripciones(
        self,
        fecha_desde=None,
        fecha_hasta=None,
        id_facultad=None,
        id_carrera=None,
        id_actividad=None,
        id_disciplina=None,
    ):
        connection = get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            filtros = []
            params = []

            if fecha_desde is not None:
                filtros.append("p.fecha >= %s")
                params.append(fecha_desde)

            if fecha_hasta is not None:
                filtros.append("p.fecha <= %s")
                params.append(fecha_hasta)

            if id_facultad is not None:
                filtros.append("f.id_facultad = %s")
                params.append(id_facultad)

            if id_carrera is not None:
                filtros.append("c.id_carrera = %s")
                params.append(id_carrera)

            if id_actividad is not None:
                filtros.append("p.id_actividad = %s")
                params.append(id_actividad)

            if id_disciplina is not None:
                filtros.append("d.id_disciplina = %s")
                params.append(id_disciplina)

            where_sql = "WHERE i.fecha_baja IS NULL"
            if filtros:
                where_sql += " AND " + " AND ".join(filtros)

            cursor.execute(
                f"""
                SELECT i.id_inscripcion,
                       i.fecha_inscripcion,
                       i.fecha_baja,
                       i.estado,
                       i.id_estudiante,
                       i.id_practica,
                       p.fecha AS fecha_practica,
                       p.id_actividad,
                      c.id_carrera,
                      f.id_facultad,
                      d.id_disciplina,
                       a.nombre AS actividad_nombre,
                       a.dia,
                       a.hora_inicio,
                       a.hora_fin,
                       a.estado AS estado_actividad,
                       e.documento AS ci,
                       e.nombre AS estudiante_nombre,
                       e.apellido AS estudiante_apellido,
                       c.nombre AS carrera_nombre,
                       f.nombre AS facultad_nombre,
                       d.nombre AS disciplina_nombre
                FROM inscripcion i
                INNER JOIN estudiante e ON e.id_estudiante = i.id_estudiante
                INNER JOIN carrera c ON c.id_carrera = e.id_carrera
                INNER JOIN facultad f ON f.id_facultad = c.id_facultad
                INNER JOIN practica p ON p.id_practica = i.id_practica
                INNER JOIN actividad a ON a.id_actividad = p.id_actividad
                INNER JOIN disciplina d ON d.id_disciplina = a.id_disciplina
                {where_sql}
                ORDER BY p.fecha, a.hora_inicio, i.id_inscripcion
                """,
                params
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
                SELECT i.id_inscripcion, i.fecha_inscripcion, i.fecha_baja,
                       i.estado, i.id_estudiante, i.id_practica,
                       p.fecha AS fecha_practica,
                       p.id_actividad,
                       a.nombre AS actividad_nombre,
                       a.dia,
                       a.hora_inicio,
                       a.hora_fin,
                       a.estado AS estado_actividad
                FROM inscripcion i
                INNER JOIN practica p ON p.id_practica = i.id_practica
                INNER JOIN actividad a ON a.id_actividad = p.id_actividad
                WHERE i.id_inscripcion = %s
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
                SELECT i.id_inscripcion, i.fecha_inscripcion, i.fecha_baja,
                       i.estado, i.id_estudiante, i.id_practica,
                       p.fecha AS fecha_practica,
                       p.id_actividad,
                       a.nombre AS actividad_nombre,
                       a.dia,
                       a.hora_inicio,
                       a.hora_fin,
                       a.estado AS estado_actividad
                FROM inscripcion i
                INNER JOIN practica p ON p.id_practica = i.id_practica
                INNER JOIN actividad a ON a.id_actividad = p.id_actividad
                WHERE i.id_estudiante = %s AND i.fecha_baja IS NULL
                ORDER BY i.fecha_inscripcion, i.id_inscripcion
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
                SELECT i.id_inscripcion, i.fecha_inscripcion, i.fecha_baja,
                       i.estado, i.id_estudiante, i.id_practica,
                       p.fecha AS fecha_practica,
                       p.id_actividad,
                       a.nombre AS actividad_nombre,
                       a.dia,
                       a.hora_inicio,
                       a.hora_fin,
                       a.estado AS estado_actividad
                FROM inscripcion i
                INNER JOIN practica p ON p.id_practica = i.id_practica
                INNER JOIN actividad a ON a.id_actividad = p.id_actividad
                WHERE i.id_practica = %s AND i.fecha_baja IS NULL
                ORDER BY i.fecha_inscripcion, i.id_inscripcion
                """,
                (id_practica,)
            )
            return cursor.fetchall()
        finally:
            connection.close()

    def get_inscripciones_confirmadas_con_asistencia_by_practica(self, id_practica):
        connection = get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT i.id_inscripcion,
                       i.fecha_inscripcion,
                       i.fecha_baja,
                       i.estado,
                       i.id_estudiante,
                       i.id_practica,
                       e.documento AS ci,
                       e.nombre AS estudiante_nombre,
                       e.apellido AS estudiante_apellido,
                       c.nombre AS carrera_nombre,
                       f.nombre AS facultad_nombre,
                       asis.id_asistencia,
                       COALESCE(asis.presente, 0) AS presente
                FROM inscripcion i
                INNER JOIN estudiante e ON e.id_estudiante = i.id_estudiante
                INNER JOIN carrera c ON c.id_carrera = e.id_carrera
                INNER JOIN facultad f ON f.id_facultad = c.id_facultad
                LEFT JOIN asistencia asis ON asis.id_inscripcion = i.id_inscripcion
                WHERE i.id_practica = %s
                  AND i.fecha_baja IS NULL
                  AND i.estado = 'confirmada'
                ORDER BY e.apellido, e.nombre, i.id_inscripcion
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
                                SELECT id_inscripcion, estado
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
                WHERE id_practica = %s
                  AND fecha_baja IS NULL
                  AND estado = 'confirmada'
                """,
                (id_practica,)
            )
            return cursor.fetchone()["total"]
        finally:
            connection.close()

    def get_inscripciones_activas_by_estudiante(self, id_estudiante):
        connection = get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT i.id_inscripcion, i.fecha_inscripcion, i.fecha_baja,
                       i.estado, i.id_estudiante, i.id_practica,
                       p.fecha AS fecha_practica,
                       p.id_actividad,
                       a.nombre AS actividad_nombre,
                       a.dia,
                       a.hora_inicio,
                       a.hora_fin,
                       a.estado AS estado_actividad
                FROM inscripcion i
                INNER JOIN practica p ON p.id_practica = i.id_practica
                INNER JOIN actividad a ON a.id_actividad = p.id_actividad
                WHERE i.id_estudiante = %s
                  AND i.fecha_baja IS NULL
                ORDER BY p.fecha, a.hora_inicio, i.id_inscripcion
                """,
                (id_estudiante,)
            )
            return cursor.fetchall()
        finally:
            connection.close()

    def get_inscripcion_en_espera_anterior(self, id_practica):
        connection = get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT id_inscripcion, id_estudiante
                FROM inscripcion
                WHERE id_practica = %s
                  AND fecha_baja IS NULL
                  AND estado = 'en_espera'
                ORDER BY fecha_inscripcion, id_inscripcion
                LIMIT 1
                """,
                (id_practica,)
            )
            return cursor.fetchone()
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