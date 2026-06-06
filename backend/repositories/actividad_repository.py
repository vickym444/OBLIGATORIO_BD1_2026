from database.connection import get_connection


def get_all_actividades():
    connection = get_connection()
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT id_actividad, nombre, cupo_maximo, cupo_minimo, hora_inicio, hora_fin, dia, estado
            FROM actividad
            ORDER BY id_actividad
            """
        )
        return cursor.fetchall()
    finally:
        connection.close()