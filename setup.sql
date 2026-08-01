CREATE TABLE Manufacturers(
    `name` VARCHAR(255) PRIMARY KEY,
    `country` VARCHAR(255),
    `address` VARCHAR(255)
)


-- Component table holds meta data for all components --
CREATE TABLE Components(
    `component_id` int AUTO_INCREMENT PRIMARY KEY,
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
    `component_id` int PRIMARY KEY,
    `form_factor` varchar(32),
    `socket_type` varchar(16),
    -- RAM --
    `ddr_version` int,
    `ram_slots` int,
    -- PCIe --
    `PCIe_1_gen` float,
    `PCIe_1_slots` int,
    `PCIe_4_gen` float,
    `PCIe_4_slots` int,
    `PCIe_8_gen` float,
    `PCIe_8_slots` int,
    `PCIe_16_gen` float,
    `PCIe_16_slots` int,
    -- Storage --
    `M_2_slots` int,
    `SATA_6_ports` int,
    `SATA_3_ports` int,
    `U_2_ports` int
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
    `component_id` int PRIMARY KEY,
    `capacity_MB` int,
    `ddr_version` int,
    `speed_MHz` int
);

CREATE TABLE CPU(
    `component_id` int PRIMARY KEY,
    `socket_type` varchar(16),
    `cores` int,
    `clock_speed_MHz` int,
    -- RAM Compatibility --
    `max_ram_capacity_MB` int,
    `ddr_version` int
);

CREATE TABLE Storage(
    `component_id` int PRIMARY KEY,
    `capacity_GB` int,
    `storage_type` varchar(16),
    `form_factor` varchar(16),
    `interface` varchar(32),
    `cache_MB` int,
    `nvme` boolean
);

CREATE TABLE GPU(
    `component_id` int PRIMARY KEY,
    `clock_speed_MHz` int,
    `vram_GB` int,
    `vram_type` varchar(16),
    `PCIe_gen` float,
    `PCIe_lanes` int
);

CREATE TABLE PSU(
    'component_id' int,
    `wattage` int,
    `form_factor` VARCHAR(16),
    `efficiency_rating` VARCHAR(16),
    -- Connectors --
    `atx_24_pin` int,
    `eps_8_pin` int,
    `pcie_12vhpwr` int,
    `pcie_6_plus_2` int,
    `sata` int,
    `molex_4_pin` int
)