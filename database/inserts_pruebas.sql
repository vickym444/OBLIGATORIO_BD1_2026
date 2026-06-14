-- -----------------------------------------------------
-- Inserts de prueba
-- -----------------------------------------------------

-- facultad
INSERT INTO `bd1_2026`.`facultad` (`nombre`) VALUES ('Facultad de Ingenieria');
INSERT INTO `bd1_2026`.`facultad` (`nombre`) VALUES ('Facultad de Ciencias');

-- carrera
INSERT INTO `bd1_2026`.`carrera` (`nombre`, `id_facultad`) VALUES ('Informatica', 1);
INSERT INTO `bd1_2026`.`carrera` (`nombre`, `id_facultad`) VALUES ('Sistemas', 1);

-- disciplina
INSERT INTO `bd1_2026`.`disciplina` (`nombre`, `descripcion`) VALUES ('Futbol', 'Deporte de equipo');
INSERT INTO `bd1_2026`.`disciplina` (`nombre`, `descripcion`) VALUES ('Natacion', 'Deporte acuatico');

-- espacio
INSERT INTO `bd1_2026`.`espacio` (`nombre`, `descripcion`) VALUES ('Cancha 1', 'Cancha de futbol 11');
INSERT INTO `bd1_2026`.`espacio` (`nombre`, `descripcion`) VALUES ('Piscina', 'Piscina 25 mts');


-- estudiante
INSERT INTO `bd1_2026`.`estudiante` (`documento`, `nombre`, `apellido`, `email`, `activo`, `id_carrera`) VALUES ('12345678', 'Juan', 'Perez', 'juan@mgail.com', 1, 1);
INSERT INTO `bd1_2026`.`estudiante` (`documento`, `nombre`, `apellido`, `email`, `activo`, `id_carrera`) VALUES ('87654321', 'Maria', 'Garcia', 'maria@adinet.com.uy', 1, 2);

-- actividad
INSERT INTO `bd1_2026`.`actividad` (`nombre`, `cupo_maximo`, `cupo_minimo`, `dia`, `hora_inicio`, `hora_fin`, `estado`, `id_disciplina`, `id_espacio`) VALUES ('Futbol matutino', 20, 10, 'Lunes y Miercoles', '08:00:00', '09:30:00', 'abierta', 1, 1);
INSERT INTO `bd1_2026`.`actividad` (`nombre`, `cupo_maximo`, `cupo_minimo`, `dia`, `hora_inicio`, `hora_fin`, `estado`, `id_disciplina`, `id_espacio`) VALUES ('Natacion vespertina', 15, 5, 'Martes y Jueves', '17:00:00', '18:30:00', 'abierta', 2, 2);

-- practica
INSERT INTO `bd1_2026`.`practica` (`id_actividad`, `fecha`) VALUES (1, '2026-06-08');
INSERT INTO `bd1_2026`.`practica` (`id_actividad`, `fecha`) VALUES (1, '2026-06-10');
INSERT INTO `bd1_2026`.`practica` (`id_actividad`, `fecha`) VALUES (2, '2026-06-09');
INSERT INTO `bd1_2026`.`practica` (`id_actividad`, `fecha`) VALUES (2, '2026-06-11');


-- inscripcion
INSERT INTO `bd1_2026`.`inscripcion` (`fecha_inscripcion`, `fecha_baja`, `estado`, `id_estudiante`, `id_practica`) VALUES ('2026-06-01', NULL, 'confirmada', 1, 1);
INSERT INTO `bd1_2026`.`inscripcion` (`fecha_inscripcion`, `fecha_baja`, `estado`, `id_estudiante`, `id_practica`) VALUES ('2026-06-01', NULL, 'confirmada', 2, 3);

-- asistencia
INSERT INTO `bd1_2026`.`asistencia` (`presente`, `id_inscripcion`) VALUES (1, 1);
INSERT INTO `bd1_2026`.`asistencia` (`presente`, `id_inscripcion`) VALUES (1, 2);

-- facultad
INSERT INTO `bd1_2026`.`facultad` (`nombre`, `activo`) VALUES ('Facultad de Arquitectura', 1);
INSERT INTO `bd1_2026`.`facultad` (`nombre`, `activo`) VALUES ('Facultad de Humanidades', 0);

-- carrera
INSERT INTO `bd1_2026`.`carrera` (`nombre`, `id_facultad`, `activo`) VALUES ('Arquitectura Computacional', 3, 1);
INSERT INTO `bd1_2026`.`carrera` (`nombre`, `id_facultad`, `activo`) VALUES ('Historia de la Cultura', 4, 0);

-- disciplina
INSERT INTO `bd1_2026`.`disciplina` (`nombre`, `descripcion`, `activo`) VALUES ('Voleibol', 'Deporte de red y equipo', 1);
INSERT INTO `bd1_2026`.`disciplina` (`nombre`, `descripcion`, `activo`) VALUES ('Atletismo', 'Pruebas de pista y campo', 0);

-- espacio
INSERT INTO `bd1_2026`.`espacio` (`nombre`, `descripcion`, `activo`) VALUES ('Gimnasio Central', 'Espacio cubierto multiuso', 1);
INSERT INTO `bd1_2026`.`espacio` (`nombre`, `descripcion`, `activo`) VALUES ('Pista Atletica', 'Pista exterior para atletismo', 0);

-- estudiante
INSERT INTO `bd1_2026`.`estudiante` (`documento`, `nombre`, `apellido`, `email`, `activo`, `id_carrera`) VALUES ('11223344', 'Diego', 'Alvarez', 'diego.alvarez@correo.com', 1, 3);
INSERT INTO `bd1_2026`.`estudiante` (`documento`, `nombre`, `apellido`, `email`, `activo`, `id_carrera`) VALUES ('44332211', 'Sofia', 'Mendez', 'sofia.mendez@correo.com', 0, 4);

-- usuario
-- Passwords de prueba: admin123 / alumno123
INSERT INTO `bd1_2026`.`usuario` (`email`, `password_hash`, `rol`, `id_estudiante`, `activo`) VALUES ('admin@bd1.uy', '$2b$12$eJhY1hYZdPpyXttyScPwluseKylydAx25J.xQsVT5XaNreem8dDJ2', 'admin', NULL, 1);
INSERT INTO `bd1_2026`.`usuario` (`email`, `password_hash`, `rol`, `id_estudiante`, `activo`) VALUES ('juan.perez@correo.com', '$2b$12$wIlvioRa53naLMlF.erpjOl/LhrgIAynld5A3MLTiF2dlfeoSVQqm', 'estudiante', 1, 1);
INSERT INTO `bd1_2026`.`usuario` (`email`, `password_hash`, `rol`, `id_estudiante`, `activo`) VALUES ('maria.garcia@correo.com', '$2b$12$wIlvioRa53naLMlF.erpjOl/LhrgIAynld5A3MLTiF2dlfeoSVQqm', 'estudiante', 2, 1);
INSERT INTO `bd1_2026`.`usuario` (`email`, `password_hash`, `rol`, `id_estudiante`, `activo`) VALUES ('sofia.mendez@correo.com', '$2b$12$wIlvioRa53naLMlF.erpjOl/LhrgIAynld5A3MLTiF2dlfeoSVQqm', 'estudiante', 4, 0);

-- actividad
INSERT INTO `bd1_2026`.`actividad` (`nombre`, `cupo_maximo`, `cupo_minimo`, `dia`, `hora_inicio`, `hora_fin`, `estado`, `id_disciplina`, `id_espacio`, `activo`) VALUES ('Voleibol mixto', 18, 8, 'Martes y Jueves', '19:00:00', '20:30:00', 'abierta', 3, 3, 1);
INSERT INTO `bd1_2026`.`actividad` (`nombre`, `cupo_maximo`, `cupo_minimo`, `dia`, `hora_inicio`, `hora_fin`, `estado`, `id_disciplina`, `id_espacio`, `activo`) VALUES ('Atletismo entrenamiento', 12, 4, 'Lunes y Miercoles', '07:00:00', '08:00:00', 'cerrada', 4, 4, 1);
INSERT INTO `bd1_2026`.`actividad` (`nombre`, `cupo_maximo`, `cupo_minimo`, `dia`, `hora_inicio`, `hora_fin`, `estado`, `id_disciplina`, `id_espacio`, `activo`) VALUES ('Futbol nocturno', 14, 7, 'Viernes', '20:00:00', '21:30:00', 'abierta', 1, 1, 1);
INSERT INTO `bd1_2026`.`actividad` (`nombre`, `cupo_maximo`, `cupo_minimo`, `dia`, `hora_inicio`, `hora_fin`, `estado`, `id_disciplina`, `id_espacio`, `activo`) VALUES ('Voleibol recreativo', 16, 8, 'Viernes', '18:00:00', '19:30:00', 'cancelada', 3, 3, 0);

-- practica
INSERT INTO `bd1_2026`.`practica` (`id_actividad`, `fecha`, `activo`) VALUES (3, '2026-06-12', 1);
INSERT INTO `bd1_2026`.`practica` (`id_actividad`, `fecha`, `activo`) VALUES (3, '2026-06-19', 1);
INSERT INTO `bd1_2026`.`practica` (`id_actividad`, `fecha`, `activo`) VALUES (4, '2026-06-13', 1);
INSERT INTO `bd1_2026`.`practica` (`id_actividad`, `fecha`, `activo`) VALUES (5, '2026-06-20', 0);

-- inscripcion
INSERT INTO `bd1_2026`.`inscripcion` (`fecha_inscripcion`, `fecha_baja`, `estado`, `id_estudiante`, `id_practica`) VALUES ('2026-06-10', NULL, 'confirmada', 3, 5);
INSERT INTO `bd1_2026`.`inscripcion` (`fecha_inscripcion`, `fecha_baja`, `estado`, `id_estudiante`, `id_practica`) VALUES ('2026-06-11', NULL, 'en_espera', 2, 6);
INSERT INTO `bd1_2026`.`inscripcion` (`fecha_inscripcion`, `fecha_baja`, `estado`, `id_estudiante`, `id_practica`) VALUES ('2026-06-12', '2026-06-21', 'cancelada', 4, 8);
INSERT INTO `bd1_2026`.`inscripcion` (`fecha_inscripcion`, `fecha_baja`, `estado`, `id_estudiante`, `id_practica`) VALUES ('2026-06-13', NULL, 'confirmada', 1, 7);

-- asistencia
INSERT INTO `bd1_2026`.`asistencia` (`presente`, `id_inscripcion`) VALUES (1, 3);
INSERT INTO `bd1_2026`.`asistencia` (`presente`, `id_inscripcion`) VALUES (0, 6);

