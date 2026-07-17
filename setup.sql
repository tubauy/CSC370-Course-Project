CREATE TABLE Motherboards(
    `name` varchar(256) PRIMARY KEY,
    `socket` varchar(64),
    `ddr_version` int
);

CREATE TABLE RAM(
    `name` varchar(256) PRIMARY KEY,
    `capacity_MB` int,
    `ddr_version` int
);

CREATE TABLE CPU(
    `name` varchar(256) PRIMARY KEY,
    `socket` varchar(64),
    `clock_speed_Hz` int,
    `ddr_version` int
);