CREATE DATABASE if not exists parc_informatique;

USE parc_informatique;

CREATE TABLE IF NOT EXISTS machines (
    `id` INT(10) AUTO_INCREMENT PRIMARY KEY,
    `nom` VARCHAR(256) NOT NULL,  
    `ip` VARCHAR(16),  
    `nombre_cpu` INT(4),  
    `taille_ram` VARCHAR(10),  
    `os` VARCHAR(128),  
    `version` VARCHAR(16)  
);

CREATE TABLE IF NOT EXISTS disques (
    `id` INT(10) AUTO_INCREMENT PRIMARY KEY,
    `nom` VARCHAR(256) NOT NULL,  
    `taille` VARCHAR(16),  
    `machine_id` INT(10),
    FOREIGN KEY (`machine_id`) REFERENCES machines(`id`) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS applications (
    `id` INT(10) AUTO_INCREMENT PRIMARY KEY,
    `nom` VARCHAR(256) NOT NULL,  
    `editeur` VARCHAR(256),   
    `version` VARCHAR(16)  
);

CREATE TABLE IF NOT EXISTS machine_application (
    `id_machine` INT(10) NOT NULL,
    `id_application` INT(10) NOT NULL,
    FOREIGN KEY (`id_machine`) REFERENCES machines(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`id_application`) REFERENCES applications(`id`) ON DELETE CASCADE
)