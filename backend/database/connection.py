git add backend/repositories/disciplina_repository.py backend/schemas/disciplina_schema.py backend/services/disciplina_service.py backend/routes/disciplina_routes.py backend/main.py backend/database/connection.pyimport os

import mysql.connector

from dotenv import load_dotenv
load_dotenv()


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "bd1_2026"),
    )


def test_connection():
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        return {"status": "ok", "database": os.getenv("DB_NAME", "bd1_2026"), "result": result[0] if result else None}
    finally:
        connection.close()