-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema coronavirus
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema coronavirus
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `coronavirus` DEFAULT CHARACTER SET utf8 ;
USE `coronavirus` ;

-- -----------------------------------------------------
-- Table `coronavirus`.`Paises`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `coronavirus`.`Paises` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nomepaises` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `coronavirus`.`Casos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `coronavirus`.`Casos` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `quantidades` VARCHAR(45) NOT NULL,
  `data` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `data_UNIQUE` (`data` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `coronavirus`.`Mortes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `coronavirus`.`Mortes` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `quantidade` VARCHAR(45) NOT NULL,
  `data` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `coronavirus`.`Recuperados`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `coronavirus`.`Recuperados` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `quantidade` VARCHAR(45) NOT NULL,
  `data` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `data_UNIQUE` (`data` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `coronavirus`.`Paises_has_Casos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `coronavirus`.`Paises_has_Casos` (
  `Paises_id` INT NOT NULL,
  `Casos_id` INT NOT NULL,
  PRIMARY KEY (`Paises_id`, `Casos_id`),
  INDEX `fk_Paises_has_Casos_Casos1_idx` (`Casos_id` ASC) VISIBLE,
  INDEX `fk_Paises_has_Casos_Paises_idx` (`Paises_id` ASC) VISIBLE,
  CONSTRAINT `fk_Paises_has_Casos_Paises`
    FOREIGN KEY (`Paises_id`)
    REFERENCES `coronavirus`.`Paises` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Paises_has_Casos_Casos1`
    FOREIGN KEY (`Casos_id`)
    REFERENCES `coronavirus`.`Casos` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `coronavirus`.`Paises_has_Mortes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `coronavirus`.`Paises_has_Mortes` (
  `Paises_id` INT NOT NULL,
  `Mortes_id` INT NOT NULL,
  PRIMARY KEY (`Paises_id`, `Mortes_id`),
  INDEX `fk_Paises_has_Mortes_Mortes1_idx` (`Mortes_id` ASC) VISIBLE,
  INDEX `fk_Paises_has_Mortes_Paises1_idx` (`Paises_id` ASC) VISIBLE,
  CONSTRAINT `fk_Paises_has_Mortes_Paises1`
    FOREIGN KEY (`Paises_id`)
    REFERENCES `coronavirus`.`Paises` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Paises_has_Mortes_Mortes1`
    FOREIGN KEY (`Mortes_id`)
    REFERENCES `coronavirus`.`Mortes` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `coronavirus`.`Paises_has_Recuperados`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `coronavirus`.`Paises_has_Recuperados` (
  `Paises_id` INT NOT NULL,
  `Recuperados_id` INT NOT NULL,
  PRIMARY KEY (`Paises_id`, `Recuperados_id`),
  INDEX `fk_Paises_has_Recuperados_Recuperados1_idx` (`Recuperados_id` ASC) VISIBLE,
  INDEX `fk_Paises_has_Recuperados_Paises1_idx` (`Paises_id` ASC) VISIBLE,
  CONSTRAINT `fk_Paises_has_Recuperados_Paises1`
    FOREIGN KEY (`Paises_id`)
    REFERENCES `coronavirus`.`Paises` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Paises_has_Recuperados_Recuperados1`
    FOREIGN KEY (`Recuperados_id`)
    REFERENCES `coronavirus`.`Recuperados` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
