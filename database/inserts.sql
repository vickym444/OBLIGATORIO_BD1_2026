USE `bd1_2026`;

-- =====================================================
-- DATOS DE PRUEBA COMPLETOS
-- =====================================================
-- Nota: pensado para cargar sobre esquema vacio (recien creado con schema.sql).

-- -----------------------------------------------------
-- 1) FACULTADES (5)
-- -----------------------------------------------------
INSERT INTO `facultad` (`nombre`, `activo`) VALUES
('Facultad de Ingenieria', 1),
('Facultad de Ciencias', 1),
('Facultad de Arquitectura', 1),
('Facultad de Humanidades', 1),
('Facultad de Economia', 1);

-- -----------------------------------------------------
-- 2) CARRERAS (15, 3 por facultad)
-- -----------------------------------------------------
INSERT INTO `carrera` (`nombre`, `id_facultad`, `activo`) VALUES
('Ingenieria en Computacion', 1, 1),
('Ingenieria Electrica', 1, 1),
('Ingenieria Civil', 1, 1),
('Licenciatura en Biologia', 2, 1),
('Licenciatura en Fisica', 2, 1),
('Licenciatura en Quimica', 2, 1),
('Arquitectura', 3, 1),
('Diseno Industrial', 3, 1),
('Urbanismo', 3, 1),
('Historia', 4, 1),
('Filosofia', 4, 1),
('Letras', 4, 1),
('Contador Publico', 5, 1),
('Administracion', 5, 1),
('Economia', 5, 1);

-- -----------------------------------------------------
-- 3) DISCIPLINAS (10)
-- -----------------------------------------------------
INSERT INTO `disciplina` (`nombre`, `descripcion`, `activo`) VALUES
('Futbol', 'Deporte de equipo en cancha grande', 1),
('Natacion', 'Entrenamiento en piscina', 1),
('Tenis', 'Practica individual y dobles', 1),
('Voleibol', 'Deporte de red en equipo', 1),
('Basquetbol', 'Deporte de equipo en cancha cerrada', 1),
('Handball', 'Deporte de equipo en cancha', 1),
('Atletismo', 'Pista y campo', 1),
('Yoga', 'Practica de movilidad y respiracion', 1),
('Ajedrez', 'Disciplina estrategica', 1),
('Gimnasia Funcional', 'Acondicionamiento fisico general', 1);

-- -----------------------------------------------------
-- 4) ESPACIOS (10)
-- -----------------------------------------------------
INSERT INTO `espacio` (`nombre`, `descripcion`, `activo`) VALUES
('Cancha Futbol 1', 'Cancha de cesped sintetico', 1),
('Cancha Futbol 2', 'Cancha alternativa de futbol', 1),
('Piscina Olimpica', 'Piscina principal de 50 metros', 1),
('Piscina Cerrada', 'Piscina techada de 25 metros', 1),
('Cancha Tenis A', 'Superficie rapida', 1),
('Cancha Tenis B', 'Superficie de polvo de ladrillo', 1),
('Gimnasio Central', 'Cancha multiproposito cubierta', 1),
('Pista Atletica', 'Pista de 400 metros', 1),
('Salon Bienestar', 'Sala para yoga y funcional', 1),
('Sala Estrategia', 'Espacio para ajedrez y analisis', 1);

-- -----------------------------------------------------
-- 5) ESTUDIANTES (100) + USUARIOS ESTUDIANTE (100)
--    Distribucion: id_carrera = ((n-1) % 15) + 1
-- -----------------------------------------------------
WITH RECURSIVE seq_100 AS (
	SELECT 1 AS n
	UNION ALL
	SELECT n + 1 FROM seq_100 WHERE n < 100
)
INSERT INTO `estudiante` (`documento`, `nombre`, `apellido`, `email`, `activo`, `id_carrera`)
SELECT
	CONCAT('DOC', LPAD(n, 6, '0')) AS documento,
	CONCAT('Estudiante', LPAD(n, 3, '0')) AS nombre,
	CONCAT('Apellido', LPAD(n, 3, '0')) AS apellido,
	CONCAT('estudiante', LPAD(n, 3, '0'), '@bd1.uy') AS email,
	1 AS activo,
	((n - 1) % 15) + 1 AS id_carrera
FROM seq_100;

-- Password para estudiantes: alumno123
-- Hash bcrypt (mismo usado en inserts_pruebas.sql)
INSERT INTO `usuario` (`email`, `password_hash`, `rol`, `id_estudiante`, `activo`)
SELECT
	e.email,
	'$2b$12$wIlvioRa53naLMlF.erpjOl/LhrgIAynld5A3MLTiF2dlfeoSVQqm',
	'estudiante',
	e.id_estudiante,
	1
FROM `estudiante` e;

-- -----------------------------------------------------
-- 6) USUARIO ADMIN (1)
-- -----------------------------------------------------
-- Password admin: admin123
INSERT INTO `usuario` (`email`, `password_hash`, `rol`, `id_estudiante`, `activo`) VALUES
('admin@bd1.uy', '$2b$12$eJhY1hYZdPpyXttyScPwluseKylydAx25J.xQsVT5XaNreem8dDJ2', 'admin', NULL, 1);

-- -----------------------------------------------------
-- 7) ACTIVIDADES (30)
--    Incluye varios casos con mismo dia y mismo horario en espacios distintos.
-- -----------------------------------------------------
INSERT INTO `actividad`
(`nombre`, `cupo_maximo`, `cupo_minimo`, `hora_inicio`, `hora_fin`, `dia`, `estado`, `id_disciplina`, `id_espacio`, `activo`)
VALUES
('Futbol mixto matutino A', 24, 12, '08:00:00', '09:30:00', 'Lunes y Miercoles', 'abierta', 1, 1, 1),
('Futbol mixto matutino B', 24, 12, '08:00:00', '09:30:00', 'Lunes y Miercoles', 'abierta', 1, 2, 1),
('Futbol femenino tarde', 22, 10, '18:00:00', '19:30:00', 'Martes y Jueves', 'abierta', 1, 1, 1),
('Futbol masculino noche', 22, 10, '20:00:00', '21:30:00', 'Martes y Jueves', 'abierta', 1, 2, 1),

('Natacion inicial A', 18, 8, '07:00:00', '08:00:00', 'Lunes', 'abierta', 2, 3, 1),
('Natacion inicial B', 18, 8, '07:00:00', '08:00:00', 'Lunes', 'abierta', 2, 4, 1),
('Natacion intermedio', 16, 8, '17:00:00', '18:00:00', 'Miercoles y Viernes', 'abierta', 2, 3, 1),
('Natacion avanzada', 14, 6, '19:00:00', '20:00:00', 'Miercoles y Viernes', 'abierta', 2, 4, 1),

('Tenis principiantes A', 12, 6, '09:00:00', '10:30:00', 'Martes', 'abierta', 3, 5, 1),
('Tenis principiantes B', 12, 6, '09:00:00', '10:30:00', 'Martes', 'abierta', 3, 6, 1),
('Tenis dobles', 10, 4, '18:30:00', '20:00:00', 'Jueves', 'abierta', 3, 5, 1),

('Voleibol mixto A', 20, 10, '18:00:00', '19:30:00', 'Lunes y Miercoles', 'abierta', 4, 7, 1),
('Voleibol mixto B', 20, 10, '18:00:00', '19:30:00', 'Lunes y Miercoles', 'abierta', 4, 1, 1),
('Voleibol recreativo', 20, 10, '10:00:00', '11:30:00', 'Viernes', 'abierta', 4, 7, 1),

('Basquetbol abierto A', 20, 10, '16:00:00', '17:30:00', 'Martes y Jueves', 'abierta', 5, 7, 1),
('Basquetbol abierto B', 20, 10, '16:00:00', '17:30:00', 'Martes y Jueves', 'abierta', 5, 2, 1),
('Basquetbol competitivo', 16, 8, '20:00:00', '21:30:00', 'Viernes', 'abierta', 5, 7, 1),

('Handball universitario A', 18, 8, '17:00:00', '18:30:00', 'Lunes y Miercoles', 'abierta', 6, 7, 1),
('Handball universitario B', 18, 8, '17:00:00', '18:30:00', 'Lunes y Miercoles', 'abierta', 6, 2, 1),
('Handball nocturno', 16, 8, '21:00:00', '22:00:00', 'Jueves', 'abierta', 6, 7, 1),

('Atletismo pista A', 25, 12, '07:30:00', '09:00:00', 'Martes y Jueves', 'abierta', 7, 8, 1),
('Atletismo pista B', 25, 12, '07:30:00', '09:00:00', 'Martes y Jueves', 'abierta', 7, 1, 1),
('Atletismo velocidad', 15, 8, '18:00:00', '19:00:00', 'Viernes', 'abierta', 7, 8, 1),

('Yoga matinal A', 20, 8, '08:30:00', '09:30:00', 'Lunes y Miercoles', 'abierta', 8, 9, 1),
('Yoga matinal B', 20, 8, '08:30:00', '09:30:00', 'Lunes y Miercoles', 'abierta', 8, 10, 1),
('Yoga vespertino', 20, 8, '19:00:00', '20:00:00', 'Martes y Jueves', 'abierta', 8, 9, 1),

('Ajedrez estrategia A', 30, 10, '15:00:00', '16:30:00', 'Miercoles', 'abierta', 9, 10, 1),
('Ajedrez estrategia B', 30, 10, '15:00:00', '16:30:00', 'Miercoles', 'abierta', 9, 9, 1),

('Funcional campus A', 22, 10, '12:00:00', '13:00:00', 'Martes y Jueves', 'abierta', 10, 9, 1),
('Funcional campus B', 22, 10, '12:00:00', '13:00:00', 'Martes y Jueves', 'abierta', 10, 7, 1),
('Funcional nocturno', 18, 8, '20:30:00', '21:30:00', 'Lunes', 'abierta', 10, 9, 1);

-- -----------------------------------------------------
-- 8) PRACTICAS para 20 actividades, en ventana dinamica
--    [hoy - 1 mes, hoy + 1 mes]
-- -----------------------------------------------------
-- 4 fechas por actividad (2 pasadas aprox + 2 futuras aprox)
INSERT INTO `practica` (`id_actividad`, `fecha`, `activo`)
SELECT
	a.id_actividad,
	DATE_ADD(CURDATE(), INTERVAL d.offset_dias DAY) AS fecha,
	1
FROM `actividad` a
JOIN (
	SELECT -28 AS offset_dias UNION ALL
	SELECT -14 UNION ALL
	SELECT 7 UNION ALL
	SELECT 21
) d
WHERE a.id_actividad BETWEEN 1 AND 20;

-- -----------------------------------------------------
-- 9) INSCRIPCIONES
--    - muchas en practicas pasadas
--    - algunas en practicas futuras
-- -----------------------------------------------------
-- Pasadas: volumen alto, mezcla confirmada / en_espera / cancelada
INSERT INTO `inscripcion` (`fecha_inscripcion`, `fecha_baja`, `estado`, `id_estudiante`, `id_practica`)
SELECT
	DATE_SUB(p.fecha, INTERVAL ((e.id_estudiante + p.id_practica) % 10 + 1) DAY) AS fecha_inscripcion,
	CASE
		WHEN MOD(e.id_estudiante + p.id_practica, 17) = 0 THEN DATE_SUB(p.fecha, INTERVAL 1 DAY)
		ELSE NULL
	END AS fecha_baja,
	CASE
		WHEN MOD(e.id_estudiante + p.id_practica, 17) = 0 THEN 'cancelada'
		WHEN MOD(e.id_estudiante + p.id_practica, 7) = 0 THEN 'en_espera'
		ELSE 'confirmada'
	END AS estado,
	e.id_estudiante,
	p.id_practica
FROM `practica` p
JOIN `estudiante` e
	ON MOD(e.id_estudiante + p.id_practica, 5) = 0
WHERE p.fecha < CURDATE();

-- Futuras: menor volumen, mayormente confirmadas
INSERT INTO `inscripcion` (`fecha_inscripcion`, `fecha_baja`, `estado`, `id_estudiante`, `id_practica`)
SELECT
	DATE_SUB(CURDATE(), INTERVAL MOD(e.id_estudiante + p.id_practica, 5) DAY) AS fecha_inscripcion,
	NULL AS fecha_baja,
	CASE
		WHEN MOD(e.id_estudiante + p.id_practica, 11) = 0 THEN 'en_espera'
		ELSE 'confirmada'
	END AS estado,
	e.id_estudiante,
	p.id_practica
FROM `practica` p
JOIN `estudiante` e
	ON MOD(e.id_estudiante + p.id_practica, 13) = 0
WHERE p.fecha >= CURDATE();

-- -----------------------------------------------------
-- 10) ASISTENCIAS aleatorias para practicas pasadas
-- -----------------------------------------------------
INSERT INTO `asistencia` (`presente`, `id_inscripcion`)
SELECT
	CASE WHEN MOD(i.id_inscripcion, 3) = 0 THEN 0 ELSE 1 END AS presente,
	i.id_inscripcion
FROM `inscripcion` i
JOIN `practica` p ON p.id_practica = i.id_practica
WHERE p.fecha < CURDATE()
	AND i.estado IN ('confirmada', 'cancelada')
	AND MOD(i.id_inscripcion, 2) = 0;

-- =====================================================
-- CREDENCIALES DE PRUEBA
-- =====================================================
-- ADMIN
-- email: admin@bd1.uy
-- password: admin123

-- ESTUDIANTES (5 ejemplos)
-- 1) email: estudiante001@bd1.uy | password: alumno123
-- 2) email: estudiante002@bd1.uy | password: alumno123
-- 3) email: estudiante003@bd1.uy | password: alumno123
-- 4) email: estudiante004@bd1.uy | password: alumno123
-- 5) email: estudiante005@bd1.uy | password: alumno123