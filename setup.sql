CREATE TABLE IF NOT EXISTS `Motherboards` (
	`component_id` INTEGER AUTO_INCREMENT,
	`name` VARCHAR(128),
	`form_factor` VARCHAR(32),
	`socket_type` VARCHAR(16),
	`ddr_version` INTEGER,
	`ram_slots` INTEGER,
	`PCIe_1_gen` FLOAT,
	`PCIe_1_slots` INTEGER,
	`PCIe_4_gen` FLOAT,
	`PCIe_4_slots` INTEGER,
	`PCIe_8_gen` FLOAT,
	`PCIe_8_slots` INTEGER,
	`PCIe_16_gen` FLOAT,
	`PCIe_16_slots` INTEGER,
	`M_2_slots` INTEGER,
	`SATA_6_ports` INTEGER,
	`SATA_3_ports` INTEGER,
	`U_2_ports` INTEGER,
	PRIMARY KEY(`component_id`)
) AUTO_INCREMENT = 1;


CREATE TABLE IF NOT EXISTS `RAM` (
	`component_id` INTEGER AUTO_INCREMENT,
	`name` VARCHAR(128),
	`capacity_MB` INTEGER,
	`ddr_version` INTEGER,
	`speed_MHz` INTEGER,
	PRIMARY KEY(`component_id`)
) AUTO_INCREMENT = 10;


CREATE TABLE IF NOT EXISTS `CPU` (
	`component_id` INTEGER AUTO_INCREMENT,
	`name` VARCHAR(128),
	`socket_type` VARCHAR(16),
	`cores` INTEGER,
	`clock_speed_MHz` INTEGER,
	`max_ram_capacity_MB` INTEGER,
	`ddr_version` INTEGER,
	PRIMARY KEY(`component_id`)
) AUTO_INCREMENT = 20;


CREATE TABLE IF NOT EXISTS `Storage` (
	`component_id` INTEGER AUTO_INCREMENT,
	`name` VARCHAR(128),
	`capacity_GB` INTEGER,
	`storage_type` VARCHAR(16),
	`form_factor` VARCHAR(16),
	`interface` VARCHAR(32),
	`cache_MB` INTEGER,
	`nvme` BOOLEAN,
	PRIMARY KEY(`component_id`)
) AUTO_INCREMENT = 30;


CREATE TABLE IF NOT EXISTS `GPU` (
	`component_id` INTEGER AUTO_INCREMENT,
	`name` VARCHAR(128),
	`clock_speed_MHz` INTEGER,
	`vram_GB` INTEGER,
	`vram_type` VARCHAR(16),
	`PCIe_gen` FLOAT,
	`PCIe_4` BOOLEAN NOT NULL,
	`PCIe_8` BOOLEAN NOT NULL,
	`PCIe_16` BOOLEAN NOT NULL,
	PRIMARY KEY(`component_id`)
) AUTO_INCREMENT = 40;


CREATE TABLE IF NOT EXISTS `Configurations` (
	`Config_id` INTEGER AUTO_INCREMENT,
	`Motherboard_id` INTEGER,
	`CPU_id` INTEGER,
	`GPU_id` INTEGER,
	`RAM_id` INTEGER,
	`Storage_id` INTEGER,
	PRIMARY KEY(`Config_id`)
);


ALTER TABLE `Configurations`
ADD FOREIGN KEY(`Motherboard_id`) REFERENCES `Motherboards`(`component_id`)
ON UPDATE SET NULL ON DELETE SET NULL;
ALTER TABLE `Configurations`
ADD FOREIGN KEY(`CPU_id`) REFERENCES `CPU`(`component_id`)
ON UPDATE SET NULL ON DELETE SET NULL;
ALTER TABLE `Configurations`
ADD FOREIGN KEY(`GPU_id`) REFERENCES `GPU`(`component_id`)
ON UPDATE SET NULL ON DELETE SET NULL;
ALTER TABLE `Configurations`
ADD FOREIGN KEY(`RAM_id`) REFERENCES `RAM`(`component_id`)
ON UPDATE SET NULL ON DELETE SET NULL;
ALTER TABLE `Configurations`
ADD FOREIGN KEY(`Storage_id`) REFERENCES `Storage`(`component_id`)
ON UPDATE SET NULL ON DELETE SET NULL;