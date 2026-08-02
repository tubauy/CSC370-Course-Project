CREATE TABLE Users(
    `user_id` INT AUTO_INCREMENT PRIMARY KEY,
    `username` VARCHAR(255),
    `email` VARCHAR(255),
    `date_created` DATETIME
)

CREATE TABLE Configurations(
    `configuration_id` INT AUTO_INCREMENT PRIMARY KEY,
    -- Owner of configuration -- 
    `user_id` INT REFERENCES `Users`(`user_id`)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    -- Component IDs --
    `motherboard_id` INT REFERENCES `Motherboards`(`component_id`)
        ON DELETE SET NULL
        ON UPDATE SET NULL,
    `ram_id` INT REFERENCES `RAM`(`component_id`)
        ON DELETE SET NULL
        ON UPDATE SET NULL,
    `cpu_id` INT REFERENCES `CPUs`(`component_id`)
        ON DELETE SET NULL
        ON UPDATE SET NULL,
    `storage_id` INT REFERENCES `Storage`(`component_id`)
        ON DELETE SET NULL
        ON UPDATE SET NULL,
    `gpu_id` INT REFERENCES `GPUs`(`component_id`)
        ON DELETE SET NULL
        ON UPDATE SET NULL,
    `psu_id` INT REFERENCES `PSUs`(`component_id`)
        ON DELETE SET NULL
        ON UPDATE SET NULL,
)

CREATE TABLE Manufacturers(
    `name` VARCHAR(255) PRIMARY KEY,
    `country` VARCHAR(255),
    `address` VARCHAR(255)
)

-- Component table holds meta data for all components --
CREATE TABLE Components(
    `component_id` INT AUTO_INCREMENT PRIMARY KEY,
    `part_type` ENUM(
        'Motherboard', 
        'RAM', 
        'CPU', 
        'Storage', 
        'GPU', 
        'PSU'
    ),
    `name` VARCHAR(255),
    `manufacturer` VARCHAR(255),
    `pirce` FLOAT,
    `release_date` DATE
)

CREATE TABLE Motherboards(
    `component_id` INT PRIMARY KEY,
    `form_factor` VARCHAR(32),
    `socket_type` VARCHAR(16),
    -- RAM --
    `ddr_version` INT,
    `ram_slots` INT,
    -- PCIe --
    `PCIe_1_gen` FLOAT,
    `PCIe_1_slots` INT,
    `PCIe_4_gen` FLOAT,
    `PCIe_4_slots` INT,
    `PCIe_8_gen` FLOAT,
    `PCIe_8_slots` INT,
    `PCIe_16_gen` FLOAT,
    `PCIe_16_slots` INT,
    -- Storage --
    `M_2_slots` INT,
    `SATA_6_ports` INT,
    `SATA_3_ports` INT,
    `U_2_ports` INT
    -- Network --
    `ethernet_speed` ENUM(
        '10 Gb/s',
        '5 Gb/s',
        '2.5 Gb/s',
        '1 Gb/s',
        '100 Mb/s',
        'N/A'
    )
    `WiFi` VARCHAR(32)
);

CREATE TABLE RAM(
    `component_id` INT PRIMARY KEY,
    `capacity_MB` INT,
    `ddr_version` INT,
    `speed_MHz` INT
);

CREATE TABLE CPUs(
    `component_id` INT PRIMARY KEY,
    `socket_type` VARCHAR(16),
    `cores` INT,
    `clock_speed_MHz` INT,
    -- RAM Compatibility --
    `max_ram_capacity_MB` INT,
    `ddr_version` INT
);

CREATE TABLE Storage(
    `component_id` INT PRIMARY KEY,
    `capacity_GB` INT,
    `storage_type` VARCHAR(16),
    `form_factor` VARCHAR(16),
    `INTerface` VARCHAR(32),
    `cache_MB` INT,
    `nvme` BOOLEAN
);

CREATE TABLE GPUs(
    `component_id` INT PRIMARY KEY,
    `clock_speed_MHz` INT,
    `vram_GB` INT,
    `vram_type` VARCHAR(16),
    `PCIe_gen` FLOAT,
    `PCIe_lanes` INT
);

CREATE TABLE PSUs(
    'component_id' INT,
    `wattage` INT,
    `form_factor` VARCHAR(16),
    `efficiency_rating` VARCHAR(16),
    -- Connectors --
    `atx_24_pin` INT,
    `eps_8_pin` INT,
    `pcie_12vhpwr` INT,
    `pcie_6_plus_2` INT,
    `sata` INT,
    `molex_4_pin` INT
)