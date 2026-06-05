

-- -----------------------------------------------------
-- Modificar tabla actividad: eliminar fecha, agregar dia
-- -----------------------------------------------------

ALTER TABLE  `bd1_2026`.`actividad`
    DROP COLUMN `fecha`,
    ADD COLUMN `dia` ENUM(
        'Lunes',
        'Martes',
        'Miercoles',
        'Jueves',
        'Viernes',
        'Lunes y Miercoles',
        'Martes y Jueves',
        'Miercoles y Viernes'
        ) NOT NULL AFTER `hora_fin`;

-- -----------------------------------------------------
-- Crear tabla practica
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bd1_2026`.`practica` (
     `id_practica` INT NOT NULL AUTO_INCREMENT,
     `id_actividad` INT NOT NULL,
     `fecha` DATE NOT NULL,
     PRIMARY KEY (`id_practica`),
     INDEX `fk_practica_actividad_idx` (`id_actividad` ASC) VISIBLE,
     CONSTRAINT `fk_practica_actividad`
         FOREIGN KEY (`id_actividad`)
             REFERENCES `bd1_2026`.`actividad` (`id_actividad`)
             ON DELETE NO ACTION
             ON UPDATE NO ACTION
) ENGINE = InnoDB;


-- -----------------------------------------------------
-- Modificar inscripcion: cambio FK de actividad por FK de practica
-- -----------------------------------------------------

ALTER TABLE `bd1_2026`.`inscripcion`
    DROP FOREIGN KEY `fk_inscripcion_actividad1`,
    DROP INDEX `fk_inscripcion_actividad1_idx`,
    DROP COLUMN `id_actividad`,
    ADD COLUMN `id_practica` INT NOT NULL AFTER `id_estudiante`,
    ADD INDEX `fk_inscripcion_practica_idx` (`id_practica` ASC) VISIBLE,
    ADD CONSTRAINT `fk_inscripcion_practica`
        FOREIGN KEY (`id_practica`)
            REFERENCES `bd1_2026`.`practica` (`id_practica`)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION;


-- -----------------------------------------------------
-- Modificar asistencia: garantizar relacion 1:1 con inscripcion
-- -----------------------------------------------------
ALTER TABLE `bd1_2026`.`asistencia`
    ADD UNIQUE INDEX `id_inscripcion_UNIQUE` (`id_inscripcion` ASC) VISIBLE;