# OBLIGATORIO_BD1_2026

Sistema de gestion de actividades deportivas universitarias.
Istrucciones de ejecución local.

## Requisitos previos

- Python 3.10+ instalado
- Node.js 18+ y npm
- MySQL 8.0+
- Git (opcional, para clonar el repositorio)

## 1) Clonar o descargar el proyecto

```bash
git clone <URL_DEL_REPO>
cd OBLIGATORIO_BD1_2026
```

Si ya lo tenés descargado, solo entrá a la carpeta raiz del proyecto.

## 2) Crear base de datos y cargar scripts

Desde la raiz del proyecto, ejecutar:

```bash
mysql -u root -p < database/schema.sql
mysql -u root -p < database/inserts.sql
```

Esto crea la base `bd1_2026` y carga datos de prueba.

## 3) Configurar backend

Entrar a la carpeta de backend:

```bash
cd backend
```

Crear un archivo `.env` en `backend/` con este contenido (ajustá usuario/password de MySQL según tu PC):

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=tu_password_mysql
DB_NAME=bd1_2026

JWT_SECRET_KEY=change-this-in-production
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60

HOST=0.0.0.0
PORT=8000
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Ejecutar backend:

```bash
python main.py
```

El backend queda en:

- http://localhost:8000
- Health check DB: http://localhost:8000/health/db

## 4) Configurar frontend

En otra terminal, desde la raiz del proyecto:

```bash
cd frontend
npm install
npm run dev
```

El frontend queda en:

- http://localhost:5173

## 5) Credenciales de prueba

Las credenciales cargadas por `database/inserts.sql` son:

- Admin:
	- Email: `admin@bd1.uy`
	- Password: `admin123`
- Estudiantes:
	- `estudiante001@bd1.uy` / `alumno123`
	- `estudiante002@bd1.uy` / `alumno123`
	- `estudiante003@bd1.uy` / `alumno123`
	- `estudiante004@bd1.uy` / `alumno123`
	- `estudiante005@bd1.uy` / `alumno123`

## 6) Comandos utiles

Backend (desde `backend/`):

```bash
python main.py
```

Frontend (desde `frontend/`):

```bash
npm run dev
npm run build
```