CREATE TABLE Motherboards(
    `component_id` int PRIMARY KEY,
    `name` varchar(128),
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
    -- Headers --
);

CREATE TABLE RAM(
    `component_id` int PRIMARY KEY,
    `name` varchar(128),
    `capacity_MB` int,
    `ddr_version` int,
    `speed_MHz` int
);

CREATE TABLE CPU(
    `component_id` int PRIMARY KEY,
    `name` varchar(128),
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