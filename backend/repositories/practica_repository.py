from database.connection import get_connection


class PracticaRepository:
    def _listar_practicas_con_estadisticas(self, where_sql="", params=(), ordenar_porcentaje=False, solo_cupos_disponibles=False):
        connection = get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            order_sql = (
                "ORDER BY porcentaje_completitud DESC, p.fecha, a.hora_inicio, p.id_practica"
                if ordenar_porcentaje
                else "ORDER BY p.fecha, a.hora_inicio, p.id_practica"
            )
            
            having_clause = ""
            if solo_cupos_disponibles:
                having_clause = "HAVING inscriptos_confirmados < a.cupo_maximo"
            cursor.execute(
                f"""
                SELECT p.id_practica,
                       p.id_actividad,
                       p.fecha,
                       p.activo,
                       a.nombre AS actividad_nombre,
                       a.dia,
                       a.hora_inicio,
                       a.hora_fin,
                       a.estado AS estado_actividad,
                       a.cupo_maximo,
                       COALESCE(COUNT(CASE
                           WHEN i.estado = 'confirmada' AND i.fecha_baja IS NULL THEN 1
                       END), 0) AS inscriptos_confirmados,
                       COALESCE(
                           ROUND(
                               (COUNT(CASE
                                   WHEN i.estado = 'confirmada' AND i.fecha_baja IS NULL THEN 1
                               END) * 100.0) / NULLIF(a.cupo_maximo, 0),
                               2
                           ),
                           0
                       ) AS porcentaje_completitud
                FROM practica p
                INNER JOIN actividad a ON a.id_actividad = p.id_actividad
                LEFT JOIN inscripcion i ON i.id_practica = p.id_practica
                {where_sql}
                GROUP BY p.id_practica,
                         p.id_actividad,
                         p.fecha,
                         p.activo,
                         a.nombre,
                         a.dia,
                         a.hora_inicio,
                         a.hora_fin,
                         a.estado,
                         a.cupo_maximo
                {having_clause}
                {order_sql}
                """,
                params,
            )
            return cursor.fetchall()
        finally:
            connection.close()

    def get_all_practicas(self):
        return self._listar_practicas_con_estadisticas("WHERE p.activo = 1")

    def get_practicas_by_fecha(self, fecha):
        return self._listar_practicas_con_estadisticas("WHERE p.fecha = %s AND p.activo = 1", (fecha,))

    def get_practicas_by_fecha_ordenadas(self, fecha, ordenar_porcentaje=False, solo_cupos_disponibles=False):
        return self._listar_practicas_con_estadisticas(
            "WHERE p.fecha = %s AND p.activo = 1",
            (fecha,),
            ordenar_porcentaje=ordenar_porcentaje,
            solo_cupos_disponibles=solo_cupos_disponibles,
        )

    def get_practicas_by_rango_fechas(self, fecha_desde, fecha_hasta, ordenar_porcentaje=False, solo_cupos_disponibles=False):
        return self._listar_practicas_con_estadisticas(
            "WHERE p.fecha BETWEEN %s AND %s AND p.activo = 1",
            (fecha_desde, fecha_hasta),
            ordenar_porcentaje=ordenar_porcentaje,
            solo_cupos_disponibles=solo_cupos_disponibles,
        )

    def get_practica_by_actividad_y_fecha(self, id_actividad, fecha):
        connection = get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT id_practica, id_actividad, fecha, activo
                FROM practica
                WHERE id_actividad = %s AND fecha = %s
                """,
                (id_actividad, fecha)
            )
            return cursor.fetchone()
        finally:
            connection.close()

    def get_practica_by_actividad_y_fecha_inactiva(self, id_actividad, fecha):
        connection = get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT id_practica, id_actividad, fecha, activo
                FROM practica
                WHERE id_actividad = %s
                  AND fecha = %s
                  AND activo = 0
                """,
                (id_actividad, fecha)
            )
            return cursor.fetchone()
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

    def reactivate_practica(self, id_practica, id_actividad, fecha):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                UPDATE practica
                SET id_actividad = %s,
                    fecha = %s,
                    activo = 1
                WHERE id_practica = %s
                """,
                (id_actividad, fecha, id_practica)
            )
            connection.commit()
            return cursor.rowcount
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