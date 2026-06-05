-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;


SET @OLD_SQL_MODE.=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema bd1_2026
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `bd1_2026` DEFAULT CHARACTER SET utf8 ;
USE `bd1_2026` ;

-- -----------------------------------------------------
-- Table `bd1_2026`.`facultad`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bd1_2026`.`facultad` (
  `id_facultad` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id_facultad`),
  UNIQUE INDEX `nombre_UNIQUE` (`nombre` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `bd1_2026`.`carrera`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bd1_2026`.`carrera` (
  `id_carrera` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(100) NOT NULL,
  `id_facultad` INT NOT NULL,
  PRIMARY KEY (`id_carrera`),
  INDEX `fk_carrera_facultad1_idx` (`id_facultad` ASC) VISIBLE,
  CONSTRAINT `fk_carrera_facultad1`
    FOREIGN KEY (`id_facultad`)
    REFERENCES `bd1_2026`.`facultad` (`id_facultad`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `bd1_2026`.`estudiante`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bd1_2026`.`estudiante` (
  `id_estudiante` INT NOT NULL AUTO_INCREMENT,
  `documento` VARCHAR(20) NOT NULL,
  `nombre` VARCHAR(50) NOT NULL,
  `apellido` VARCHAR(50) NOT NULL,
  `email` VARCHAR(100) NOT NULL,
  `activo` TINYINT NOT NULL DEFAULT 1,
  `id_carrera` INT NOT NULL,
  PRIMARY KEY (`id_estudiante`),
  UNIQUE INDEX `documento_UNIQUE` (`documento` ASC) VISIBLE,
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE,
  INDEX `fk_estudiante_carrera1_idx` (`id_carrera` ASC) VISIBLE,
  CONSTRAINT `fk_estudiante_carrera1`
    FOREIGN KEY (`id_carrera`)
    REFERENCES `bd1_2026`.`carrera` (`id_carrera`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `bd1_2026`.`disciplina`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bd1_2026`.`disciplina` (
  `id_disciplina` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(100) NOT NULL,
  `descripcion` VARCHAR(255) NULL,
  PRIMARY KEY (`id_disciplina`),
  UNIQUE INDEX `nombre_UNIQUE` (`nombre` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `bd1_2026`.`espacio`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bd1_2026`.`espacio` (
  `id_espacio` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(100) NOT NULL,
  `capacidad` INT NOT NULL,
  `descripcion` VARCHAR(255) NULL,
  PRIMARY KEY (`id_espacio`),
  UNIQUE INDEX `nombre_UNIQUE` (`nombre` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `bd1_2026`.`actividad`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bd1_2026`.`actividad` (
  `id_actividad` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(100) NOT NULL,
  `cupo_maximo` INT NOT NULL,
  `cupo_minimo` INT NOT NULL,
  `dia` ENUM('Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Lunes y Miercoles', 'Martes y Jueves', 'Miercoles y Viernes') NOT NULL,
  `hora_inicio` TIME NOT NULL,
  `hora_fin` TIME NOT NULL,
  `estado` ENUM('abierta', 'cerrada', 'finalizada', 'cancelada') NOT NULL,
  `id_disciplina` INT NOT NULL,
  `id_espacio` INT NOT NULL,
  PRIMARY KEY (`id_actividad`),
  INDEX `fk_actividad_disciplina1_idx` (`id_disciplina` ASC) VISIBLE,
  INDEX `fk_actividad_espacio1_idx` (`id_espacio` ASC) VISIBLE,
  CONSTRAINT `fk_actividad_disciplina1`
    FOREIGN KEY (`id_disciplina`)
    REFERENCES `bd1_2026`.`disciplina` (`id_disciplina`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_actividad_espacio1`
    FOREIGN KEY (`id_espacio`)
    REFERENCES `bd1_2026`.`espacio` (`id_espacio`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `bd1_2026`.`practica`
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
     ON UPDATE NO ACTION)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `bd1_2026`.`inscripcion`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bd1_2026`.`inscripcion` (
  `id_inscripcion` INT NOT NULL AUTO_INCREMENT,
  `fecha_inscripcion` DATE NOT NULL,
  `fecha_baja` DATE NULL,
  `estado` ENUM('confirmada', 'en_espera', 'cancelada') NOT NULL,
  `id_estudiante` INT NOT NULL,
  `id_practica` INT NOT NULL,
  PRIMARY KEY (`id_inscripcion`),
  INDEX `fk_inscripcion_estudiante1_idx` (`id_estudiante` ASC) VISIBLE,
  INDEX `fk_inscripcion_practica_idx` (`id_practica` ASC) VISIBLE,
  CONSTRAINT `fk_inscripcion_estudiante1`
    FOREIGN KEY (`id_estudiante`)
    REFERENCES `bd1_2026`.`estudiante` (`id_estudiante`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_inscripcion_practica`
    FOREIGN KEY (`id_practica`)
    REFERENCES `bd1_2026`.`practica` (`id_practica`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `bd1_2026`.`asistencia`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bd1_2026`.`asistencia` (
  `id_asistencia` INT NOT NULL AUTO_INCREMENT,
  `presente` TINYINT NOT NULL,
  `id_inscripcion` INT NOT NULL,
  PRIMARY KEY (`id_asistencia`),
  UNIQUE INDEX `fk_asistencia_inscripcion1_idx` (`id_inscripcion` ASC) VISIBLE,
  CONSTRAINT `fk_asistencia_inscripcion1`
    FOREIGN KEY (`id_inscripcion`)
    REFERENCES `bd1_2026`.`inscripcion` (`id_inscripcion`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
