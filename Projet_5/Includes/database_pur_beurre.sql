SET NAMES utf8;

CREATE DATABASE IF NOT EXISTS `pur_beurre`;

USE `pur_beurre`;

CREATE TABLE `categories`
(
    `id` INT NOT NULL AUTO_INCREMENT,
    `category_name` VARCHAR(50) NOT NULL,
    PRIMARY KEY (`id`)
)
ENGINE=InnoDB;

CREATE TABLE `foodstuffs`
(
	`id` INT NOT NULL,
    `foodstuff_id` INT NOT NULL AUTO_INCREMENT,
    `foodstuff_name` VARCHAR(100) NOT NULL,
    `foodstuff_category` VARCHAR(50) NOT NULL,
	`foodstuff_description` VARCHAR(250) NOT NULL,
    PRIMARY KEY (`foodstuff_id`),
    FOREIGN KEY (`id`) REFERENCES `categories`(`id`)
)
ENGINE=InnoDB;

CREATE TABLE `substitutes`
(
    `substitute_id` INT NOT NULL AUTO_INCREMENT,
    `substitute_name` VARCHAR(50) NOT NULL,
    `substitute_nutriscore` CHAR(1) NOT NULL,
    `substitute_description` VARCHAR(250) NOT NULL,
    `substitute_store` VARCHAR(50) NOT NULL,
    `substitute_url` VARCHAR(200) NOT NULL,
    PRIMARY KEY (`substitute_id`)
    
)
ENGINE=InnoDB;
