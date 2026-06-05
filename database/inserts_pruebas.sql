-- -----------------------------------------------------
-- Inserts de prueba 1ra parte
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
INSERT INTO `bd1_2026`.`espacio` (`nombre`, `capacidad`, `descripcion`) VALUES ('Cancha 1', 22, 'Cancha de futbol 11');
INSERT INTO `bd1_2026`.`espacio` (`nombre`, `capacidad`, `descripcion`) VALUES ('Piscina', 30, 'Piscina 25 mts');

-- -----------------------------------------------------
-- Inserts de prueba 2da parte
-- -----------------------------------------------------

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

